ARG IMAGE=ubuntu:24.04
FROM ${IMAGE}

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    wget \
    g++ \
    libeigen3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and compile a simple C++ program
RUN echo '#include <iostream>' > fincpp.cpp && \
    echo '' >> fincpp.cpp && \
    echo 'int main() {' >> fincpp.cpp && \
    echo '    std::cout << "Hello, fincpp!" << std::endl;' >> fincpp.cpp && \
    echo '    return 0;' >> fincpp.cpp && \
    echo '}' >> fincpp.cpp && \
    g++ fincpp.cpp -o fincpp

CMD ["./fincpp"]