# Push this repository to GitHub

Suggested name: **digital-asic-design-flow**.

Suggested GitHub description:

> UART ASIC implementation study with Cadence Genus and Innovus: RTL synthesis, timing constraints, area analysis, scan insertion, and physical design.

DFT and physical implementation are planned in the README; the completed results currently cover synthesis.

## Prepared local repository

This folder is initialized on `main` and contains an initial commit. Create an **empty** GitHub repository under your account using the name above. Leave GitHub's “Add a README”, license, and `.gitignore` options unselected because these files are already prepared here.

Open a terminal in this folder. Replace `YOUR_USERNAME` with your GitHub username:

```sh
git remote add origin https://github.com/YOUR_USERNAME/digital-asic-design-flow.git
git push -u origin main
```

If you chose another repository name, use its exact URL instead. GitHub may ask you to sign in through your normal Git authentication method.

## If using the ZIP

Extract the archive completely, including its hidden `.git` directory, then open the extracted `digital-asic-design-flow` folder and use the two commands above.

If a copying/extraction method discarded `.git`, recreate the local history first:

```sh
git init -b main
git add .
git commit -m "Document UART RTL synthesis and prepare ASIC implementation stages"
```

Then connect the remote and push as above.

## Add future work

Put new DFT evidence under `labs/lab02-dft-insertion/` and physical implementation evidence under `labs/lab03-physical-design/`. Update the corresponding README and the root status table, then:

```sh
git add labs/lab02-dft-insertion README.md
git commit -m "Document DFT scan synthesis and scan stitching"
git push
```

Use the physical-design folder for the following stage. Do not overwrite the captured synthesis baseline with later results; add new experiment or checkpoint directories.
