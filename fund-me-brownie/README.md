This brownie project implements the following features:
- the person deploying the contract is remembered as its owner
- people can fund the contract (minimum amount of participation of 50$ is enforced)
- the contract's owner can then withdraw the funds

It is a very simple version of a crowdfunding application that can be improved by enforcing a minimum amount of contributions so that if the total amount of funding is lower than the amount the contract's owner requires all of the ETH will be returned to its original owner. A system of reward can be put in place too and we can even think about generating a token representing a stake in the funded project so that each donator can later benefit from its donation if the business succeeds.

Other difficulties was to implement testing on both local chains and test nets and, therefore, to handle deploying mock contracts and making our scripts adaptable to many different configurations. Ability to do so is nevertheless curcial because, as blokchain is immutable, testing is primordial before deploying a smart contract on a real chain.
