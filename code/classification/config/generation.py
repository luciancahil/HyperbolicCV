schedulers = {

    "exponential": (
        [1],
        [0.99]
    )}
"""    "cos_sim": ([1], [1]),
    "None": ([1], [1]),
    "cosine": ([1], [1]),

    "step": (
        [100, 150],
        [0.1, 0.2]
    ),
    """
""""plateau": (
        [10, 20],
        [0.1]
    )
}"""
             

datasets = ["Tiny-ImageNet"] #["CIFAR-10", "CIFAR-100", "Tiny-ImageNet"]
lrs = [10**i for i in range(-9, 1, 3)]
lrs.append(0.1)

seeds = [2]#[i for i in range(1, 4)]

original_text = open("Empty.txt")
original_text = original_text.read()

counts = 0
for seed in seeds:
    for lr in lrs:
        for dataset in datasets:
            for scheduler in schedulers.keys():
                setting = schedulers[scheduler]
                epochs = setting[0]
                gammas = setting[1]
                for epoch in epochs:
                    for gamma in gammas:
                        counts += 1

                        name = f"{dataset}_{scheduler}_{lr}_{gamma}_{epoch}_{seed}"

                        config_text = original_text.format(name, seed, lr, scheduler, epoch, gamma, dataset)

                        file_name = f"Exp_{name}.txt"

                        print(file_name)
                        with open(file_name, "w") as f:
                            f.write(config_text)


print(counts)