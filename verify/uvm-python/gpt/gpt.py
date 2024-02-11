import openai
import os

openai.api_key  = os.getenv('OPENAI_API_KEY')

if openai.api_key is None:
    raise Exception("You must set your OpenAI API key.")

def generate_top_v():
    # read RTL file and generate top.v
    with open("/home/rady/work/uvm_unit/EF_PWM32/hdl/rtl/bus_wrappers/EF_PWM32_apb.pp.v", "r") as file:
        rtl_content = file.read()

    prompt = f""" you would be given an RTL toplevel file written in RTL, you would need to generate a testbench file named top.v \
        The top.v file should be written in Verilog. with the following format\
            `timescale 1ns/1ps \
            module top(); \
            wire .... ; \
            wire .... ; \
            Module_Name uut(.signal1(signal1).....\
            `ifndef SKIP_WAVE_DUMP\
                initial begin \
                $dumpfile ({"waves.vcd"});\
            $dumpvars(0, top);\
        end\
    `endif\
    always #10 clk = !clk; // clk generator\
    endmodule \
    replace clk with the name used for clock. \
    don't leave any signal without connection. \
    don't ignore the `ifdef and its block indintation.\
    stick to the format provided\
    RTL file {rtl_content}"""
    rsp = get_completion(prompt)
    with open("top.v", "w") as file:
        file.write(rsp)

def generate_seq_item():
    with open("/home/rady/work/uvm_unit/EF_PWM32/EF_PWM32.json", "r") as file:
        json_file = file.read()
    with open("/home/rady/work/uvm_unit/EF_PWM32/readme.md", "r") as file:
        readme = file.read()
    with open("/home/rady/work/uvm_unit/EF_PWM32/verify/uvm-python/pwm32_item.py", "r") as file:
        seq_item = file.read()
    with open("/home/rady/work/uvm_unit/EF_PWM32/verify/uart_monitor.py", "r") as file:
        uart_mon = file.read()
    with open("/home/rady/work/uvm_unit/EF_PWM32/verify/uvm-python/pwm_interface/pwm32_if.py", "r") as file:
        interface = file.read()
    prompt = f"""you would be given a readme file that describes an RTL hardware design, a json file that describes the design. a sequence item and interface written in uvm-python.You first task is to write a monitor for the design interface whithout apb signals. you would also given a monitor that was written for uart as an example.
    The generate monitor should calculate each item defined in the sequence item and send it when the whole item is done. and use interface signals only.
    json file :```{json_file}```
    readme file: ```{readme}```
    sequence item: ```{seq_item}```
    interface : ```{interface}```
    uart monitor: ```{uart_mon}```
    """
    rsp = get_completion(prompt, model="gpt-4")
    with open("summary.log", "w") as file:
        file.write(rsp)

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


# generate_top_v()
generate_seq_item()
