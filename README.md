# 🎲 protodummy

> A cutting-edge Python library for effortlessly generating random, realistic data for your Protocol Buffer (protobuf) messages.

[![PyPI version](https://img.shields.io/pypi/v/protodummy.svg)](https://pypi.org/project/protodummy/)
[![Python Version](https://img.shields.io/pypi/pyversions/protodummy.svg)](https://pypi.org/project/protodummy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🚀 **Lightning Fast:** Seamlessly populate massive protobuf structures.
- 🧠 **Smart Generation:** Powered by `faker` to generate realistic names, emails, addresses, and more, automatically inferred from your field names.
- 🛠️ **Deeply Customizable:** Easily override rules for specific fields when you need exact constraints.
- 📦 **Zero-Friction:** Works flawlessly with standard `protobuf` compiler outputs.

## 📥 Installation

Simply install via pip (or your favorite package manager):

```bash
pip install protodummy
```

## ⚡ Quickstart

Assume you have a `user.proto` file:

```protobuf
syntax = "proto3";

message UserProfile {
    string id = 1;
    string full_name = 2;
    string email_address = 3;
    int32 age = 4;
}
```

Now, generate a random user profile in Python in two lines:

```python
from my_protos import user_pb2
from protodummy import generate_dummy

# 🪄 Magic!
random_user = generate_dummy(user_pb2.UserProfile)

print(random_user.full_name)     # e.g. "Jane Doe"
print(random_user.email_address) # e.g. "jane.doe@example.com"
print(random_user.age)           # e.g. 42
```

## 🤝 Contributing

Contributions are completely welcome! Please feel free to open a Pull Request or an Issue to help us make `protodummy` even better.

## 📄 License

This project is licensed under the [MIT License](LICENSE).
