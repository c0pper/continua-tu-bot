from transformers import AutoTokenizer, AutoModelWithLMHead, pipeline

tokenizer = AutoTokenizer.from_pretrained("LorenzoDeMattei/GePpeTto")
model = AutoModelWithLMHead.from_pretrained("LorenzoDeMattei/GePpeTto")

text_generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
prompt = "Lorenzo Valitutto è un bambino molto"