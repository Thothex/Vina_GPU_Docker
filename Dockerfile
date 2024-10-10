FROM nvidia/cuda:11.5.2-devel-ubuntu20.04

ENV TZ=Europe/Berlin
# Установка нужной временной зоны и подавление интерактивного ввода
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata
RUN apt-get update && apt-get install -y opencl-headers ocl-icd-libopencl1 ocl-icd-opencl-dev
# Установка временной зоны (замените на нужную)
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub && \
    apt-get update && \
    apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get install -y \
    build-essential \
    wget \
    nano \
    cmake \
    git \
    clinfo \
    opencl-headers \
    libboost-program-options-dev && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://archives.boost.io/release/1.77.0/source/boost_1_77_0.tar.gz && \
    tar -xvzf boost_1_77_0.tar.gz && \
    cd boost_1_77_0 && \
    ./bootstrap.sh --prefix=/boost_1_77_0 && \
    ./b2 install
RUN export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

RUN git clone https://github.com/DeltaGroupNJUPT/Vina-GPU-2.1.git

WORKDIR /Vina-GPU-2.1/QuickVina2-GPU-2.1

RUN apt update && \
    apt install -y ocl-icd-opencl-dev && \
    apt install -y libboost-dev && \
    apt install -y libboost-system-dev && \
    apt install -y libboost-filesystem-dev && \
    apt install -y libnvidia-compute-535


RUN sed -i 's|^WORK_DIR=.*|WORK_DIR=/Vina-GPU-2.1/QuickVina2-GPU-2.1|' Makefile && \
    sed -i 's|^BOOST_LIB_PATH=.*|BOOST_LIB_PATH=/boost_1_77_0|' Makefile && \
    sed -i 's|^OPENCL_LIB_PATH=.*|OPENCL_LIB_PATH=/usr/local/cuda|' Makefile

