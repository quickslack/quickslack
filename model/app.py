from flask import Flask, jsonify, request

from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import torch.nn.functional as F
from tqdm import trange
import time

app = Flask(__name__)

num_words = 50
device = torch.device('cpu')

# model.to(device)

def top_k_top_p_filtering(logits, top_k=0, top_p=0.0, filter_value=-float("Inf")):
    assert (logits.dim() == 1)
    top_k = min(top_k, logits.size(-1))
    if top_k > 0:
        indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
        logits[indices_to_remove] = filter_value

    if top_p > 0.0:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
        sorted_indices_to_remove = cumulative_probs > top_p
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0
        indices_to_remove = sorted_indices[sorted_indices_to_remove]
        logits[indices_to_remove] = filter_value
    return logits

def sample_sequence(
    model,
    length,
    context,
    num_samples=1,
    temperature=1,
    top_k=0,
    top_p=0.9,
    repetition_penalty=1.0,
    device="cuda",
):
    context = torch.tensor(context, dtype=torch.long, device=device)
    context = context.unsqueeze(0).repeat(num_samples, 1)
    generated = context
    with torch.no_grad():
        for _ in trange(length):
            inputs = {"input_ids": generated}
            outputs = model(**inputs)
            next_token_logits = outputs[0][0, -1, :] / (temperature if temperature > 0 else 1.0)
            for _ in set(generated.view(-1).tolist()):
                next_token_logits[_] /= repetition_penalty
            filtered_logits = top_k_top_p_filtering(next_token_logits, top_k=top_k, top_p=top_p)
            if temperature == 0:
                next_token = torch.argmax(filtered_logits).unsqueeze(0)
            else:
                next_token = torch.multinomial(F.softmax(filtered_logits, dim=-1), num_samples=1)
            generated = torch.cat((generated, next_token.unsqueeze(0)), dim=1)
    return generated

def get_output(input_text):
    indexed_tokens = tokenizer.encode(input_text)
    output = sample_sequence(model, num_words, indexed_tokens, device=device)
    return tokenizer.decode(
        output[0, 0:].tolist(), clean_up_tokenization_spaces=True, skip_special_tokens=True
    )

tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
model = GPT2LMHeadModel.from_pretrained("distilgpt2")
model.eval()

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        lines = request.get_json(force=True)
        print(lines)
        tracker = lines['tracker']
        latest_message = tracker['latest_message']
        input_text = latest_message['text']
        time_now = time.time()
        output_text = get_output(input_text)
        # output_text = 'this is a canned response'
        time_to_predict = time.time() - time_now
        output = output_text + ' TIME_TO_PREDICT:' + str(time_to_predict)
        return jsonify({
            "text": output,
            "buttons": [],
            "image": None,
            "elements": [],
            "attachments": []
            })

if __name__ == '__main__':
    app.run(host='0.0.0.0')