import pandas as pd
from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import Trainer, TrainingArguments
from datasets import Dataset, DatasetDict


data_pairs = pd.read_excel("dataset.xlsx")

# Convert to pandas DataFrame
df = pd.DataFrame(data_pairs)

# Split data into train and validation sets
train_df = df.sample(frac=0.8, random_state=42)
val_df = df.drop(train_df.index)

# Convert to Hugging Face datasets
train_dataset = Dataset.from_pandas(train_df)
val_dataset = Dataset.from_pandas(val_df)
datasets = DatasetDict({"train": train_dataset, "validation": val_dataset})

model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)


def preprocess_function(examples):
    inputs = ["translate English to SPARQL: " + q for q in examples["english_query"]]
    targets = [q for q in examples["sparql_query"]]
    model_inputs = tokenizer(
        inputs,
        max_length=512,
        truncation=True,
        padding="max_length"
        )

    labels = tokenizer(
        targets,
        max_length=512,
        truncation=True,
        padding="max_length"
        ).input_ids

    model_inputs["labels"] = labels
    return model_inputs


tokenized_datasets = datasets.map(preprocess_function, batched=True)

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
)

trainer.train()

# Save the model
model.save_pretrained("./sparql_t5_model")
tokenizer.save_pretrained("./sparql_t5_model")

# evalute
results = trainer.evaluate()
print(results)


# sample prediction
def generate_sparql_query(english_query):
    inputs = tokenizer(
        "translate English to SPARQL: " + english_query,
        return_tensors="pt",
        max_length=512,
        truncation=True,
        padding="max_length"
        )

    outputs = model.generate(
        inputs.input_ids,
        max_length=512,
        num_beams=4,
        early_stopping=True
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# Example usage
example_query = "Who narrated the Hadith about prayer?"
print(generate_sparql_query(example_query))
