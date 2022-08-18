`timescale 1ns/100ps

module tb;

    localparam CLK_PERIOD   = 10;
    localparam DATA_WIDTH   = 32;

    logic clk_i;
    logic rst_ni;
    logic en_i;

    logic sel;
    logic spi_ss;
    logic spi_mosi;

    logic uart_rx_inst;
    logic uart_txen;
    logic uart_tx;
    logic uart_rx;

    logic tempsense_clkref;
    logic tempsense_clkout;

    logic [7:0] gpio_o;
    logic [31:0] pattern[31:0];

    opentitan_soc_top #(
        .DATA_WIDTH (DATA_WIDTH)
    ) u_opentitan_soc_top (
        .*
    );

    initial clk_i = 0;
    initial rst_ni = 0;
    initial tempsense_clkref = 0;
    always #(CLK_PERIOD/2.0) clk_i = ~clk_i;
    always #(CLK_PERIOD/2.0) tempsense_clkref = ~tempsense_clkref;

    initial begin
        
        en_i                = 0;
        spi_ss              = 1;
        spi_mosi            = 0;
        sel                 = 0;
        uart_rx_inst        = 0;
        uart_rx             = 0;
        
        @(negedge clk_i)
        rst_ni = 1;

        #(CLK_PERIOD*10)
 
        $readmemh("../program/hex/gpio.hex", pattern);
        for (int i=0; i<32; i++) begin
            // start sending pattern i from MSB
            @(negedge clk_i)
            spi_ss = 0;
            for (int j=31; j>=0; j--) begin
                @(negedge clk_i)
                spi_mosi = pattern[i][j];
            end

            // deactivate the slave
            @(negedge clk_i)
            spi_ss = 1;
            spi_mosi = 0;

            if (pattern[i] == 32'h00000fff)
                break;
        end

        #(CLK_PERIOD*1000)
        en_i = 1;

        #(CLK_PERIOD*1000)

        if (gpio_o == 30) begin
            $display("%c[1;32m",27);
            $display("Success\n");
            $display("%c[0m",27);
        end else begin
            $display("%c[1;31m",27);
            $display("Failure\n");
            $display("%c[0m",27);
        end
	    $finish;
    end

endmodule
