Supported boards
================

Renode supports a wide array of hardware platforms, covering multiple architectures, CPU families and providing various I/O capabilities. 

This chapter contains an (incomplete) list of selected supported hardware targets - all of these include sample software binaries that run both on real hardware and in Renode.

To run example software on any of the below boards, simply run Renode and use the ``s @scripts/single-node/PLATFORM-SCRIPT-NAME.resc`` command.

The ultimate goal of Renode is to run any binary-compatible software targeted for any of those hardware platforms without modification, although of course your specific use case may require extending the provided hardware description / models.

Supported boards include:

.. raw:: html

   <style>
   .boards-table { table-layout: fixed; width: 100%; text-align: center; }
   .boards-table td { white-space: normal !important; }
   .rst-content .boards-table img { object-fit: scale-down; height: 200px !important }
   </style>

.. list-table::
   :class: boards-table

   * - .. image:: img/stm32f103.png

       `ST Micro STM3210E-EVAL <https://www.st.com/en/evaluation-tools/stm3210e-eval.html>`_
       
       `stm32f103.resc <https://github.com/renode/renode/blob/master/scripts/single-node/stm32f103.resc>`_
       
     - .. image:: img/stm_discovery.png

       `ST Micro STM32F4 Discovery <https://www.st.com/en/evaluation-tools/stm32f4discovery.html>`_

       `stm32f4_discovery.resc <https://github.com/renode/renode/blob/master/scripts/single-node/stm32f4_discovery.resc>`_

     - .. image:: img/stm32f746.png

       `ST Micro STM32F7 Discovery <https://www.st.com/en/evaluation-tools/32f746gdiscovery.html>`_

       `stm32f746.resc <https://github.com/renode/renode/blob/master/scripts/single-node/stm32f746.resc>`_
       
   * - .. image:: img/efr32mg-better.png

       `SiLabs EFR32 Mighty Gecko Wireless Starter Kit <https://www.silabs.com/products/development-tools/wireless/mesh-networking/mighty-gecko-starter-kit>`_
       
       `efr32mg.resc <https://github.com/renode/renode/blob/master/scripts/single-node/efr32mg.resc>`_
       
     - .. image:: img/sam_e70.png
     
       `Microchip SAM E70 Xplained Evaluation Kit <https://www.microchip.com/DevelopmentTools/ProductDetails/PartNO/ATSAME70-XPLD>`_
       
       `sam_e70.resc <https://github.com/renode/renode/blob/master/scripts/single-node/sam_e70.resc>`_
       
     - .. image:: img/cc2538.png
     
       `TI CC2538 Development Kit <http://www.ti.com/tool/CC2538DK>`_
       
       `cc2538.resc <https://github.com/renode/renode/blob/master/scripts/single-node/cc2538.resc>`_

   * - .. image:: img/hifive1.png

       `SiFive HiFive1 <https://www.sifive.com/boards/hifive1>`_

       `sifive_fe310.resc <https://github.com/renode/renode/blob/master/scripts/single-node/sifive_fe310.resc>`_

     - .. image:: img/hifive_unleashed.png

       `SiFive HiFive Unleashed <https://www.sifive.com/boards/hifive-unleashed>`_

       `hifive_unleashed.resc <https://github.com/renode/renode/blob/master/scripts/single-node/hifive_unleashed.resc>`_

     - .. image:: img/polarfire.png

       `Microchip PolarFire SoC Hardware Development Platform <https://www.microsemi.com/product-directory/soc-fpgas/5498-polarfire-soc-fpga#getting-started>`_

       `polarfire-soc.resc <https://github.com/renode/renode/blob/master/scripts/single-node/polarfire-soc.resc>`_

   * - .. image:: img/tegra3.jpg

       `Toradex Colibri T30 <https://www.toradex.com/computer-on-modules/colibri-arm-family/nvidia-tegra-3>`_
       
       `tegra3.resc <https://github.com/renode/renode/blob/master/scripts/single-node/tegra3.resc>`_


     - .. image:: img/vegaboard.png
     
       `OpenISA VEGAboard <https://open-isa.org/>`_

       `vegaboard_ri5cy.resc <https://github.com/renode/renode/blob/master/scripts/single-node/vegaboard_ri5cy.resc>`_

     - .. image:: img/c1000.png
     
       `Intel Quark SE Microcontroller Evaluation Kit C1000 <https://click.intel.com/edc/intel-quark-se-microcontroller-evaluation-kit-c1000.html>`_
       
       `quark_c1000.resc <https://github.com/renode/renode/blob/master/scripts/single-node/quark_c1000.resc>`_

   * - .. image:: img/fomu.png

       `Fomu <https://tomu.im/fomu.html>`_

       `renode_etherbone_fomu.resc <https://github.com/renode/renode/blob/master/scripts/complex/fomu/renode_etherbone_fomu.resc>`_

     - .. image:: img/arty.png

       `LiteX/VexRiscv <https://github.com/litex-hub/linux-on-litex-vexriscv>`_ on `Digilent Arty <https://reference.digilentinc.com/reference/programmable-logic/arty/start>`_

       `arty_litex_vexriscv.resc <https://github.com/renode/renode/blob/master/scripts/single-node/arty_litex_vexriscv.resc>`_

     - .. image:: img/zedboard.png

       `Xilinx ZedBoard <http://www.zedboard.org/product/zedboard>`_

       `zedboard.resc <https://github.com/renode/renode/blob/master/scripts/single-node/zedboard.resc>`_

And many more - Renode makes it easy to create your own platform which reuses the same peripherals / CPUs that exist in other platforms.

We provide commerical services to add new platforms - if you need help in this regard, please write to `support@renode.io <mailto:support@renode.io>`_.
