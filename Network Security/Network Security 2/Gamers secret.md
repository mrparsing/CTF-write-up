Come prima cosa ho messo le chiavi TLS su wireshark.

Poi ho filtrato i pacchetti per websocket e ho fatto follow stream.

Ho realizzato uno script python per estrarre i comandi

```jsx
import re

def extract_draw_commands(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    draw_commands = re.findall(r'42\["drawCommands",\[\[(.*?)\]\]\]', content)

    extracted_data = []

    for command in draw_commands:
        commands = command.split('],[')
        for cmd in commands:
            cmd = cmd.replace('[', '').replace(']', '')
            extracted_data.append(f"[{cmd}]")

    result = ',\n'.join(extracted_data)
    return result

file_path = 'commands.txt'

extracted_data = extract_draw_commands(file_path)

print(extracted_data)

with open('output.txt', 'w') as output_file:
    output_file.write(extracted_data)
```

Ho fatto uno script python per disegnare la flag

```jsx
import matplotlib.pyplot as plt
import ast

x_points = []
y_points = []

def draw_commands(commands):
    for command in commands:
        if command[0] == 0 and command[1] == 1 and command[2] == 12:
            x = command[3]
            y = command[4]
            x_points.append(x)
            y_points.append(y)

def read_commands_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    commands = ast.literal_eval(f"[{content}]")
    return commands

file_path = 'output.txt'

commands = read_commands_from_file(file_path)

draw_commands(commands)

plt.figure(figsize=(8, 5))
plt.plot(x_points, y_points, marker='o', linestyle='-', color='b')
plt.gca().invert_yaxis()
plt.title('Flag')
plt.show()
```