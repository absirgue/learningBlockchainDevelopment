Smart Contract Lottery, implementing the following behavior:
- the account that deployed the contract is considered as the lotery owner
- the lottery owner is the only one that can start and end the lottery
- when lottery is started, other people can buy tickets (50$ worth of ETH) to enter it
- when the lottery is closed, a winner is picked at random and takes all of the funds 

The main focus of this project is to implement a random behviour by using Chainlink VRF (Verifiable Random Function). This is particularly challenging because the blockchain is a determnistic environment hat therefore, by definition, does not support random behaviours. Chainlink VRF therefore has to be proprely use to pick a number and verify its 'random' aspect. More on https://docs.chain.link/docs/chainlink-vrf/
