name = normal_map

test:
	echo $(name)

grid:
	python3 grid_maker/grid_world_example.py "output_files/$(name).POMDP"

legacy: 
	./pomdpconvert output_files/$(name).POMDP | grep -v 'warnings found' | grep -v 'was not successfully parsed' > output_files/error_node.log || true
	cat output_files/error_node.log | cut -d '=' -f 2,3 | cut -d ' ' -f 1,2 > output_files/errors.out
	python3 grid_maker/add_missing_obs.py "output_files/$(name).POMDP" output_files/errors.out "output_files/$(name)_fixed.POMDP"
	@echo "\nActual Run"
	./pomdpconvert output_files/$(name)_fixed.POMDP

convert_to_pomdpx: grid
	./pomdpconvert output_files/$(name).POMDP

run_despot: 
	truncate output_files/despot_state_out.log --size 0	
	truncate output_files/despot_belief_out.log --size 0	
	../despot/examples/pomdpx_models/pomdpx -m output_files/$(name).POMDPx --runs 1 -v3 2>&1 | tee output_files/$(name)_despot_run.log

build_despot:
	cd ../despot/examples/pomdpx_models/ && make

clean:
	rm output_files/*
