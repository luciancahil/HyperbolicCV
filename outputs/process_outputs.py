import os
import matplotlib.pyplot as plt
import numpy as np

import matplotlib
import matplotlib as mpl

parameter_result_dict = dict()

lr_set = set()
increase_set = set()
decrease_set = set()

for file in os.listdir("outputs"):
    if file.endswith(".py"):
        continue
    print(file)

    lines = open(os.path.join("outputs", file), "r").readlines()


    # finding the line that explains the configs:
    for line in lines:
        if line.startswith("Running experiment:"):
            print(line)
            parts = line.split("_")
            seed = int(parts[-1])
            increase = float(parts[-2])
            decrease = float(parts[-3])
            lr = float(parts[-4])

            lr_set.add(lr)
            increase_set.add(increase)
            decrease_set.add(decrease)

            break



    best_line = lines[-1]

    parts = best_line.split(", ")
    print(file)
    loss = float(parts[0].split("=")[1])
    acc1 = float(parts[1].split("=")[1])
    acc5 = float(parts[2].split("=")[1])

    key = (increase, decrease, lr)

    if key in parameter_result_dict:
        parameter_result_dict[key][seed] = (loss, acc1, acc5)
    else:
        parameter_result_dict[key] = dict()
        parameter_result_dict[key][seed] = (loss, acc1, acc5)


increase_set.remove(1.1)
decrease_set.remove(0.001)

lrs = sorted(list(lr_set))
increases = sorted(list(increase_set))
decreases = sorted(list(decrease_set))



lr_place_dict = {lr: i for i, lr in enumerate(lrs)}
increase_place_dict = {increase: i for i, increase in enumerate(increases)}
decrease_place_dict = {decrease: i for i, decrease in enumerate(decreases)}



increase_heatmap_loss = [[0 for _ in range(len(increases))] for _ in range(len(lrs))]
decrease_heatmap_loss = [[0 for _ in range(len(decreases))] for _ in range(len(lrs))]

increase_heatmap_acc1 = [[0 for _ in range(len(increases))] for _ in range(len(lrs))]
decrease_heatmap_acc1 = [[0 for _ in range(len(decreases))] for _ in range(len(lrs))]

increase_heatmap_acc5 = [[0 for _ in range(len(increases))] for _ in range(len(lrs))]
decrease_heatmap_acc5 = [[0 for _ in range(len(decreases))] for _ in range(len(lrs))]

for key in parameter_result_dict:
    print(f"Results for {key}:")
    results = parameter_result_dict[key]

    losses = []
    acc1s = []
    acc5s = []
    
    for seed in results:
        loss, acc1, acc5 = results[seed]
        losses.append(loss)
        acc1s.append(acc1)
        acc5s.append(acc5)
        print(f"Seed {seed}: Loss={loss}, Acc1={acc1}, Acc5={acc5}")
    
    avg_loss = sum(losses) / len(losses)
    avg_acc1 = sum(acc1s) / len(acc1s)
    avg_acc5 = sum(acc5s) / len(acc5s)


    if(key[0] == 1.1):
        # decrease varies, increase is fixed
        decrease_heatmap_loss[lr_place_dict[key[2]]][decrease_place_dict[key[1]]] = avg_loss
        decrease_heatmap_acc1[lr_place_dict[key[2]]][decrease_place_dict[key[1]]] = avg_acc1
        decrease_heatmap_acc5[lr_place_dict[key[2]]][decrease_place_dict[key[1]]] = avg_acc5
    else:
        # increase varies, decrease is fixed
        increase_heatmap_loss[lr_place_dict[key[2]]][increase_place_dict[key[0]]] = avg_loss
        increase_heatmap_acc1[lr_place_dict[key[2]]][increase_place_dict[key[0]]] = avg_acc1
        increase_heatmap_acc5[lr_place_dict[key[2]]][increase_place_dict[key[0]]] = avg_acc5


maps = [
    (decrease_heatmap_loss, "Decrease Heatmap Loss"),
    (decrease_heatmap_acc1, "Decrease Heatmap Acc1"),
    (decrease_heatmap_acc5, "Decrease Heatmap Acc5"),
    (increase_heatmap_loss, "Increase Heatmap Loss"),
    (increase_heatmap_acc1, "Increase Heatmap Acc1"),
    (increase_heatmap_acc5, "Increase Heatmap Acc5")
]



for map in maps:

    fig, ax = plt.subplots()

    if map[1].endswith("Loss"):
        cmap = 'RdYlGn_r'
    else:
        cmap = 'RdYlGn'
    
    if map[1].startswith("Decrease"):
        x_axis_label = "Decrease"
        x_axis_vals = decreases
    else:
        x_axis_label = "Increase"
        x_axis_vals = increases

    ax.imshow(map[0], cmap=cmap)
    plt.xticks(ticks=np.arange(len(x_axis_vals)), labels=x_axis_vals)
    plt.yticks(ticks=np.arange(len(lrs)), labels=lrs)

    plt.title(map[1])
    plt.xlabel(x_axis_label)
    plt.ylabel("Learning Rate")


    for i in range(len(lrs)):
        for j in range(len(x_axis_vals)):

            text = ax.text(j, i, f"{map[0][i][j]:.2f}",
                        ha="center", va="center", color="black")



    plt.savefig(f"{map[1].replace(' ', '_')}.png", dpi=300, bbox_inches='tight')




# Heatmaps: one for x is increase y is learning rate, the other is x is decrease y is learning rate. For each heatmap, the value is the average accuracy across seeds.