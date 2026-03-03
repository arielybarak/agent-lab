import torch
import torch.nn as nn
import torch.optim as optim

# Note: This file serves as a testbed for PyTorch best practices.
# Ask Copilot to "complete the training loop" or "review against PyTorch skills".

class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(10, 5)
        self.fc2 = nn.Linear(5, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x shape: (batch_size, 10)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SimpleNet().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    # Dummy data
    inputs = torch.randn(16, 10).to(device)
    targets = torch.randn(16, 1).to(device)

    # TODO: Implement simple training loop here
    pass

if __name__ == "__main__":
    main()