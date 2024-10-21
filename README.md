# QuickVina2-GPU with Docker and NVIDIA Container Toolkit

This guide explains how to set up QuickVina2-GPU using Docker, CUDA, and the NVIDIA Container Toolkit, enabling OpenCL support for GPU acceleration.

Start by building the Docker image that includes the required CUDA and OpenCL dependencies using the following command:

DON'T forget to add the keys to the your .env file (nano .env)

```bash
docker build --build-arg AWS_ACCESS_KEY_ID=$(grep AWS_ACCESS_KEY_ID .env | cut -d '=' -f2) \
             --build-arg AWS_SECRET_ACCESS_KEY=$(grep AWS_SECRET_ACCESS_KEY .env | cut -d '=' -f2) \
             --build-arg AWS_DEFAULT_REGION=$(grep AWS_DEFAULT_REGION .env | cut -d '=' -f2) \
             --build-arg S3_URL=$(grep S3_URL .env | cut -d '=' -f2) \
             -t my-cuda-images .
```
Once the image is built, install the NVIDIA Container Toolkit to allow Docker to interact with your NVIDIA GPU. Begin by adding the GPG key:

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
```
Next, add the NVIDIA repository to your sources list:

```bash
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```
Ensure the experimental repository is enabled:

```bash
sed -i -e '/experimental/ s/^#//g' /etc/apt/sources.list.d/nvidia-container-toolkit.list
```
Then, update your package list and install the NVIDIA Container Toolkit:

```bash
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```
After installation, restart the Docker service:

```bash
sudo systemctl restart docker
```
Now you can run your Docker container with access to all available GPUs using:

```bash
docker run --gpus all \
           -e AWS_ACCESS_KEY_ID=$(grep AWS_ACCESS_KEY_ID .env | cut -d '=' -f2) \
           -e AWS_SECRET_ACCESS_KEY=$(grep AWS_SECRET_ACCESS_KEY .env | cut -d '=' -f2) \
           -e AWS_DEFAULT_REGION=$(grep AWS_DEFAULT_REGION .env | cut -d '=' -f2) \
           -e S3_URL=$(grep S3_URL .env | cut -d '=' -f2) \
           --name my-container \
           -it my-cuda-images /bin/bash
```
If you previously built QuickVina2-GPU and need to clean the build directory before recompiling, run:

Finally, to run QuickVina2-GPU with the updated configuration file, execute:

!!! Change name of your protein, before launch in the file launch_gpu.py 
protein = 'your_protein'


```bash
python3.10 launch_gpu.py
```
This command will launch QuickVina2-GPU with the specified configuration, utilizing your GPU for the computations.
