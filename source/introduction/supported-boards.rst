Supported boards
================

Renode supports a wide array of hardware platforms, covering multiple architectures, CPU families and providing various I/O capabilities. 

This chapter contains an (incomplete) list of selected supported hardware targets - all of these include sample software binaries that run both on real hardware and in Renode.

To run example software on any of the below boards, simply run Renode and use::

    s @scripts/PATH/TO/SCRIPT-NAME.resc

Tab completion is available also for filenames, so be sure to explore the available demos.

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

       `ST Micro STM32 Nucleo-64 <https://www.st.com/en/evaluation-tools/nucleo-f103rb.html>`_
       
       :script:`stm32f103.resc <single-node/stm32f103.resc>`
       
     - .. image:: img/stm_discovery.png

       `ST Micro STM32F4 Discovery <https://www.st.com/en/evaluation-tools/stm32f4discovery.html>`_

       :script:`stm32f4_discovery.resc <single-node/stm32f4_discovery.resc>`

     - .. image:: img/stm32f746.png

       `ST Micro STM32F7 Discovery <https://www.st.com/en/evaluation-tools/32f746gdiscovery.html>`_

       :script:`stm32f746.resc <single-node/stm32f746.resc>`

   * - .. image:: img/efr32mg-better.png

       `SiLabs EFR32 Mighty Gecko Wireless Starter Kit <https://www.silabs.com/products/development-tools/wireless/mesh-networking/mighty-gecko-starter-kit>`_
       
       :script:`efr32mg.resc <single-node/efr32mg.resc>`
       
     - .. image:: img/sam_e70.png
     
       `Microchip SAM E70 Xplained Evaluation Kit <https://www.microchip.com/DevelopmentTools/ProductDetails/PartNO/ATSAME70-XPLD>`_
       
       :script:`sam_e70.resc <single-node/sam_e70.resc>`
       
     - .. image:: img/cc2538.png
     
       `TI CC2538 Development Kit <http://www.ti.com/tool/CC2538DK>`_
       
       :script:`cc2538.resc <single-node/cc2538.resc>`

   * - .. image:: img/hifive1.png

       `SiFive HiFive1 <https://www.sifive.com/boards/hifive1>`_

       :script:`sifive_fe310.resc <single-node/sifive_fe310.resc>`

     - .. image:: img/hifive_unleashed.png

       `SiFive HiFive Unleashed <https://www.sifive.com/boards/hifive-unleashed>`_

       :script:`hifive_unleashed.resc <single-node/hifive_unleashed.resc>`

     - .. image:: img/polarfire.png

       `Microchip PolarFire SoC Hardware Development Platform <https://www.microsemi.com/product-directory/soc-fpgas/5498-polarfire-soc-fpga#getting-started>`_

       :script:`polarfire-soc.resc <single-node/polarfire-soc.resc>`

   * - .. image:: img/tegra3.jpg

       `Toradex Colibri T30 <https://www.toradex.com/computer-on-modules/colibri-arm-family/nvidia-tegra-3>`_
       
       :script:`tegra3.resc <single-node/tegra3.resc>`

     - .. image:: img/vegaboard.png
     
       `OpenISA VEGAboard <https://open-isa.org/>`_

       :script:`vegaboard_ri5cy.resc <single-node/vegaboard_ri5cy.resc>`

     - .. image:: img/c1000.png
     
       `Intel Quark SE Microcontroller Evaluation Kit C1000 <https://click.intel.com/edc/intel-quark-se-microcontroller-evaluation-kit-c1000.html>`_
       
       :script:`quark_c1000.resc <single-node/quark_c1000.resc>`

   * - .. image:: img/fomu.png

       `Fomu <https://tomu.im/fomu.html>`_

       :script:`renode_etherbone_fomu.resc <complex/fomu/renode_etherbone_fomu.resc>`

     - .. image:: img/arty.png

       `LiteX/VexRiscv <https://github.com/litex-hub/linux-on-litex-vexriscv>`_ on `Digilent Arty <https://reference.digilentinc.com/reference/programmable-logic/arty/start>`_

       :script:`arty_litex_vexriscv.resc <single-node/arty_litex_vexriscv.resc>`

     - .. image:: img/zedboard.png

       `Xilinx ZedBoard <http://www.zedboard.org/product/zedboard>`_

       :script:`zedboard.resc <single-node/zedboard.resc>`

   * - .. image:: img/bluepill.png

       `ST Micro STM32F103 Blue Pill <https://stm32-base.org/boards/STM32F103C8T6-Blue-Pill>`_

       :script:`stm32f103.resc <single-node/stm32f103.resc>`

     - .. image:: img/k210.png

       `Kendryte K210 <https://www.seeedstudio.com/Sipeed-MAix-BiT-for-RISC-V-AI-IoT-p-2872.html>`_

       :script:`kendryte_k210.resc <single-node/kendryte_k210.resc>`

     - .. image:: img/zolertia-firefly.jpg

       `Zolertia Firefly <https://zolertia.io/product/firefly/>`_

       :script:`zolertia.resc <single-node/zolertia.resc>`

   * - .. image:: img/quickfeather.png

       `QuickFeather Development Kit <https://www.quicklogic.com/products/eos-s3/quickfeather-development-kit/>`_

       :script:`quickfeather.resc <single-node/quickfeather.resc>`

     - .. image:: img/nexys-video.png

       `OpenPOWER Microwatt <https://github.com/antonblanchard/microwatt>`_ on `Digilent Nexys Video <https://reference.digilentinc.com/reference/programmable-logic/nexys-video/start>`_ 

       :script:`microwatt.resc <single-node/microwatt.resc>`

     - .. image:: img/microchip_icicle.png

       `Microchip PolarFire SoC Icicle Kit <https://www.microsemi.com/product-directory/soc-fpgas/5498-polarfire-soc-fpga>`_
       
       :script:`icicle-kit.resc <single-node/icicle-kit.resc>`

   * - 

     - .. image:: img/nxp_k64f.png

       `NXP FRDM-K64F <https://www.nxp.com/design/development-boards/freedom-development-boards/mcu-boards/freedom-development-platform-for-kinetis-k64-k63-and-k24-mcus:FRDM-K64F>`_
        
       `nxp_k64f.repl <https://github.com/renode/renode/blob/master/platforms/cpus/nxp-k6xf.repl>`_

     - 

And many more - Renode makes it easy to create your own platform which reuses the same peripherals / CPUs that exist in other platforms.

We provide commerical services to add new platforms - if you need help in this regard, please write to `support@renode.io <mailto:support@renode.io>`_.
