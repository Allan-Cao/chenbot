model_name = "355M"
if not os.path.isdir(os.path.join("models", model_name)):
	print(f"Downloading {model_name} model...")
	gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/124M/
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='run1')