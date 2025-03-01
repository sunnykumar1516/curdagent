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

stored_api_key = ""

with gr.Blocks() as app:
    
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Tabs():
                with gr.Tab("Main App"):
                    gr.Markdown("## AI Interaction")
                    gr.Markdown("### Created by [Sunny Kumar](https://www.linkedin.com/in/sunny-kumar-b232417a/)")
                    gr.Markdown("### <span style='color:green;'> you can add record, display record, list tables in db </span>")
                    
                    input_text = gr.Textbox(label="Enter your query")
                    examples = gr.Examples([["list all tables in databse"], ["display records from table test"], ["add records test,uniqueemail,age to table test"]], input_text)
                    output_text = gr.Textbox(label="Response")
                    submit_btn = gr.Button("Submit")
                    submit_btn.click(process_input, inputs=input_text, outputs=output_text)
                    gr.Markdown("###  db schema is name: user name, email:user email, age: age of user. <span style='color:blue;'>email is primary key </span>")
                with gr.Tab("API Keys"):
                    gr.Markdown("## Manage groq API Keys")
                    api_key_input = gr.Textbox(label="Enter API Key", type="password")
                    save_btn = gr.Button("Save API Key")
                    api_status = gr.Textbox(label="Status", interactive=False)
                    save_btn.click(set_api_key, inputs=api_key_input, outputs=api_status)

app.launch()