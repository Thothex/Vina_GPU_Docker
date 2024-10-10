# QuickVina2-GPU with Docker and NVIDIA Container Toolkit

This guide explains how to set up QuickVina2-GPU using Docker, CUDA, and the NVIDIA Container Toolkit, enabling OpenCL support for GPU acceleration.

Start by building the Docker image that includes the required CUDA and OpenCL dependencies using the following command:

```bash
docker build -t my-cuda-image .
Once the image is built, install the NVIDIA Container Toolkit to allow Docker to interact with your NVIDIA GPU. Begin by adding the GPG key:

bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
Next, add the NVIDIA repository to your sources list:

bash
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
Ensure the experimental repository is enabled:

bash
sed -i -e '/experimental/ s/^#//g' /etc/apt/sources.list.d/nvidia-container-toolkit.list
Then, update your package list and install the NVIDIA Container Toolkit:

bash
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
After installation, restart the Docker service:

bash
sudo systemctl restart docker
Now you can run your Docker container with access to all available GPUs using:

bash
docker run --gpus all -it my-cuda-image /bin/bash
If you previously built QuickVina2-GPU and need to clean the build directory before recompiling, run:

bash
make clean
To build QuickVina2-GPU from source, execute:

bash
make source
After the build process, you need to modify the configuration file 2bm2_config.txt. Update the opencl_binary_path from:

bash
opencl_binary_path = /home/shidi/Vina-GPU-2.1/QuickVina2-GPU-2.1
to:

bash
opencl_binary_path = /Vina-GPU-2.1/QuickVina2-GPU-2-1
Finally, to run QuickVina2-GPU with the updated configuration file, execute:

bash
./QuickVina2-GPU-2-1 --config ./input_file_example/2bm2_config.txt
This command will launch QuickVina2-GPU with the specified configuration, utilizing your GPU for the computations.
