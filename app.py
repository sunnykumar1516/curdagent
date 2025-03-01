import gradio as gr
import myAgent as ag
import os

def process_input(text):
    print("saved key:--",ag.stored_api_key)
    try:
        res =  ag.agent.run(text)
        
        return "text"+res.content
    except Exception as e:
        return "causing error" + str(e)
'''
iface = gr.Interface(
    fn=process_input,
    inputs=gr.Textbox(lines=2, placeholder="Enter your input here..."),
    outputs="text",
    title="Phi Agent Gradio Interface",
    description="Send input to the Phi agent and see the processed result."
)
iface.launch()'''




def set_api_key(api_key):
    os.environ["GROQ_API_KEY"] = api_key 
    return "API Key saved successfully!"

#stored_api_key = ""

with gr.Blocks() as app:
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Tabs():
                with gr.Tab("Main App"):
                    gr.Markdown("## AI Interaction")
                    input_text = gr.Textbox(label="Enter your query")
                    output_text = gr.Textbox(label="Response")
                    submit_btn = gr.Button("Submit")
                    submit_btn.click(process_input, inputs=input_text, outputs=output_text)
                
                with gr.Tab("API Keys"):
                    gr.Markdown("## Manage groq API Keys")
                    api_key_input = gr.Textbox(label="Enter API Key", type="password")
                    save_btn = gr.Button("Save API Key")
                    api_status = gr.Textbox(label="Status", interactive=False)
                    save_btn.click(set_api_key, inputs=api_key_input, outputs=api_status)

app.launch()