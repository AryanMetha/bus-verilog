module tb_reg_bus_array;
    reg clk, reset, init;
    reg [9:0] write_enable;
    reg [159:0] data_in;
    wire [159:0] reg_out;
    wire [15:0] bus_out;
    integer i, iter;
    reg [15:0] seed[0:9];

    reg_bus_array dut(
        .clk(clk),
        .reset(reset),
        .init(init),
        .write_enable(write_enable),
        .data_in(data_in),
        .reg_out(reg_out),
        .bus_out(bus_out)
    );

    initial begin
        seed[0]=16'hD54F; seed[1]=16'hDA83; seed[2]=16'h6E36; seed[3]=16'h91EF; seed[4]=16'h3876;
        seed[5]=16'h5FAC; seed[6]=16'hB4A8; seed[7]=16'h2817; seed[8]=16'h9451; seed[9]=16'h14EE;
    end

    initial begin
        clk = 0; reset = 1; init = 0; write_enable = 0;
        #5 clk = 1; #5 clk = 0; reset = 0;

        // Initialize registers
        for(i=0; i<10; i=i+1)
            data_in[16*i +: 16] = seed[i];
        init = 1; #5 clk = 1; #5 clk = 0; init = 0;

        // 10 iterations
        for(iter=0; iter<10; iter=iter+1) begin
            write_enable = 0;
            write_enable[iter] = 1'b1;
            #5 clk = 1; #5 clk = 0;
            $display("Iteration %0d, Bus value: %h", iter, bus_out);
            for(i=0;i<10;i=i+1)
                $display("reg_out[%0d] = %h", i, reg_out[16*i+:16]);
            $display("");
        end
        $finish;
    end

    always #2 clk = ~clk;
endmodule
