Cookbook
========

The Cookbook is a collection of simple recipes that demonstrate good practices to accomplish
common tasks. The examples are usually short answers to simple "How do I..." questions that go
beyond simple API descriptions but also don't need a full guide to become clear.

.. _cookbook_recipe_start_from_a_trusted_checkpoint:

Starting from a trusted checkpoint
----------------------------------

No matter which syncing strategy we use the first step is always to fetch the chain of
block headers. While this operation is relatively lightweight it can still take up to a few hours
for the mainnet chain to progress to the tip of the chain.

If we are willing to compromise on security, we can use a trusted checkpoint to start syncing from
a more recent header and then leave it up to a background process to fill the gaps eventually.

Trinity offers two ways to do that:

1. Automatically pick a recent header from `Etherscan <https://etherscan.io>`_

.. warning::

  Caution! This method relies on a 3rd party service to provide a checkpoint for us. Consider using
  a manual checkpoint for added safety.

In order to that, we need to register for an API key on `Etherscan <https://etherscan.io>`_ and
expose it through an environment variable with the name ``TRINITY_ETHERSCAN_API_KEY``.

Then run:

.. code:: sh

  trinity --sync-from-checkpoint eth://block/byetherscan/latest

2. If we do not want to rely on `Etherscan <https://etherscan.io>`_ to pick a checkpoint for us,
we can also define one manually.

For instance, to use `block 10245082 <https://etherscan.io/block/10245082>`_
 as a checkpoint we take its hash
 ``0xa65877df954e1ff2012473efee8287252eee956c0d395a5791f1103a950a1e21`` and the difficulty (score)
 ``15,835,269,727,022,672,760,774`` and run:

.. code:: sh

  trinity --sync-from-checkpoint eth://block/byhash/0xa65877df954e1ff2012473efee8287252eee956c0d395a5791f1103a950a1e21?score=15,835,269,727,022,672,760,774

.. note::

  Checkpoints can only be used with ``beam`` or ``header`` sync.

.. _cookbook_recipe_running_as_a_light_client:

Running as a light client
-------------------------

.. warning::

    It may take a **very** long time for Trinity to find an LES node with open
    slots.  This is not a bug with trinity, but rather a shortage of nodes
    serving LES. Everyone should consider running their own LES server to improve
    the health of the network.

Use the ``--sync-mode=light`` flag to instruct Trinity to run as a light node.


.. _cookbook_recipe_mainnet_vs_testnets:

Mainnet, Görli or Ropsten
-------------------------

Trinity comes with out of the box support to sync either the Ethereum Mainnet or
the Görli and Ropsten testnets. Mainnet is the default and doesn't need any flag. Use either
``-goerli`` or ``--ropsten`` to run one of the supported testnets.

.. note::

  The Görli testnet uses `Clique consensus <https://eips.ethereum.org/EIPS/eip-225>`_ and is
  considered the superior testnet.


.. code:: sh

  trinity --ropsten


.. _cookbook_recipe_running_a_custom_network:


Running a custom network
------------------------

Trinity can run custom networks via configuration file per
`EIP-1085 <https://github.com/ethereum/EIPs/issues/1085>`_.

.. code:: sh

  trinity --genesis <PATH-TO-EIP-1085-CONFIG> --data-dir <PATH-TO-DATA-DIR> --network-id <NETWORK-ID>

For a more detailed writeup, checkout the guide about :doc:`Creating a custom testnet</guides/creating_a_custom_testnet>`


.. _cookbook_recipe_connecting_to_preferred_nodes:


Connecting to preferred nodes
-----------------------------

We can use the ``--preferred-node`` command line flag to instruct Trinity to prioritize connecting
to specific nodes. This flag takes an enode URI as a single argument but can be used multiple times
to prioritize connecting to a set of specific nodes.

.. code:: sh

  trinity --preferred-node enode://a41defa74e8d9d4152699cb9a0d195377da95833769ad6b386092ac3b16c184eb4ef4b4f02889e0b5097ff50fb5847ba99694d40b61f911cdea07b444b00e676@127.0.0.1:30304


Using ``--preferred-node`` is a good way to ensure Trinity running in
``sync-mode=light`` mode connects to known peers who serve LES.


.. _cookbook_recipe_retrieving_chain_information_via_web3:


Retrieving Chain information via web3
-------------------------------------

While just running ``trinity`` already causes the node to start syncing, it doesn't let us interact
with the chain directly (apart from the JSON-RPC API).

However, we can attach an interactive shell to a running Trinity instance with the
``attach`` subcommand. The interactive ``ipython`` shell binds a
`web3 <http://web3py.readthedocs.io>`_ instance to the ``w3`` variable.

.. code:: sh

  trinity attach

Now that Trinity runs in an interactive shell mode, let's try to get some information about the
latest block by calling ``w3.eth.getBlock('latest')``.

.. code:: sh

  In [1]: w3.eth.getBlock(0)
  Out[1]:
  AttributeDict({'difficulty': 17179869184,
    'extraData': HexBytes('0x11bbe8db4e347b4e8c937c1c8370e4b5ed33adb3db69cbdb7a38e1e50b1b82fa'),
    'gasLimit': 5000,
    'gasUsed': 0,
    'hash': HexBytes('0xd4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3'),
    'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'),
    'mixHash': HexBytes('0x0000000000000000000000000000000000000000000000000000000000000000'),
    'nonce': HexBytes('0x0000000000000042'),
    'number': 0,
    'parentHash': HexBytes('0x0000000000000000000000000000000000000000000000000000000000000000'),
    'receiptsRoot': HexBytes('0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421'),
    'sha3Uncles': HexBytes('0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347'),
    'stateRoot': HexBytes('0xd7f8974fb5ac78d9ac099b9ad5018bedc2ce0a72dad1827a1709da30580f0544'),
    'timestamp': 0,
    'transactionsRoot': HexBytes('0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421'),
    'miner': '0x0000000000000000000000000000000000000000',
    'totalDifficulty': 17179869184,
    'uncles': [],
    'size': 540,
    'transactions': []})


Performance profiling
---------------------

Trinity has builtin support for performance profiling via the ``--profile`` flag. When we run Trinity
with the ``--profile`` flag it creates a ``cProfile`` of every single process in the current directory.

The files are named ``profile_*`` (e.g. ``profile_discovery``) and can be viewed with any tool that
supports ``cProfile`` files.

A simple way is through ``cprofilev``

.. code:: sh

  pip install cprofilev

Once installed we can generate a HTML based report and view it in a browser.

.. code:: sh

  cprofilev -f profile_discovery
