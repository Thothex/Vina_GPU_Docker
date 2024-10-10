Вот пример содержимого README, который вы можете напрямую вставить в ваш файл README.md на GitHub:

markdown
Копировать код
# QuickVina2-GPU with Docker and NVIDIA Container Toolkit

This guide walks you through the steps to build a Docker image for CUDA, install the NVIDIA Container Toolkit, and configure QuickVina2-GPU to run with OpenCL support.

## Prerequisites

- Docker installed on your system
- NVIDIA GPU drivers installed on the host machine
- CUDA-compatible GPU

### Step 1: Build Docker Image

First, build a Docker image with the necessary CUDA and OpenCL dependencies:

docker build -t my-cuda-image .
This command builds the Docker image using the Dockerfile in the current directory.

Step 2: Install NVIDIA Container Toolkit
To allow Docker to access your NVIDIA GPU, you need to install the NVIDIA Container Toolkit. Use the following commands:

curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
Next, add the NVIDIA repository to your sources list:

1. curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

2. sed -i -e '/experimental/ s/^#//g' /etc/apt/sources.list.d/nvidia-container-toolkit.list

3. sudo apt-get update
Now install the NVIDIA Container Toolkit:

4. sudo apt-get install -y nvidia-container-toolkit
Finally, restart the Docker service to apply the changes:

5. sudo systemctl restart docker
Step 3: Run Docker Container
Now that your Docker image is ready and the NVIDIA Container Toolkit is installed, you can run the container with GPU support:

docker run --gpus all -it my-cuda-image /bin/bash
This command will launch the container with access to all available GPUs.

Step 4: Clean Previous Builds (Optional)
If you have previously built QuickVina2-GPU, it's a good idea to clean the build directory before recompiling:

make clean
Step 5: Build QuickVina2-GPU from Source
To build QuickVina2-GPU from source, use the following command:

make source
Step 6: Update Configuration
In the configuration file 2bm2_config.txt, update the opencl_binary_path to the correct path. Replace:

opencl_binary_path = /home/shidi/Vina-GPU-2.1/QuickVina2-GPU-2.1
With:

opencl_binary_path = /Vina-GPU-2.1/QuickVina2-GPU-2.1
Step 7: Run QuickVina2-GPU
Now that everything is set up, you can run QuickVina2-GPU with the provided configuration file:

./QuickVina2-GPU-2-1 --config ./input_file_example/2bm2_config.txt
This will execute the QuickVina2-GPU using the specified configuration.





