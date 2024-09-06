# ============================================================================ #
#                         STARKNET NODE BENCHMAR RUNNER                        #
# ============================================================================ #

NODES := madara
IMGS := $(addsuffix /image.tar.gz,$(NODES))

RESET    :=\033[0m
TERTIARY :=\033[2;3;37m # dim white italic
PASS     :=\033[1;36m   # bold cyan
PASS     :=\033[1;32m   # bold green
WARN     :=\033[1;31m   # bold red

.PHONY: all
all: help

.PHONY: help
help:
	@echo "TODO(help)"

.PHONY: run
run: images
	@for node in $(NODES); do \
		echo -e "$(TERTIARY)running$(RESET) $(PASS)$$node$(RESET)"; \
		docker-compose -f $$node/compose.yaml up -d; \
	done
	@echo -e "$(PASS)all services set up$(RESET)"

.PHONY: stop
stop: images
	@for node in $(NODES); do \
		echo -e "$(TERTIARY)stopping $(WARN)$$node$(RESET)"; \
		docker-compose -f $$node/compose.yaml stop; \
	done
	@echo -e "$(WARN)all services stopped$(RESET)"

.PHONY: logs
logs: images
	@for node in $(NODES); do \
		echo -e "$(TERTIARY)logs for $(INFO)$$node$(RESET)"; \
		docker-compose -f $$node/compose.yaml logs; \
	done

.PHONY: images
images: $(IMGS)

.PHONY: clean
clean: stop
	@echo -e "$(TERTIARY)pruning containers$(RESET)"
	@docker container prune -f
	@echo -e "$(TERTIARY)removing local images tar.gz$(RESET)"
	@rm -rf $(IMGS)
	@echo -e "$(TERTIARY)pruning images$(RESET)"
	@docker image prune -f

.PHONY: re
re: clean
	@make --silent run

.PHONY: debug
debug:
	@echo $(NODES)
	@echo $(IMGS)

%image.tar.gz: node = $(@D)
%image.tar.gz: %default.nix
	@echo -e "$(TERTIARY)building$(RESET) $(PASS)$(node)$(RESET)" ;
	@nix-build $(node) -o $(node)/result
	@$(node)/result/bin/copyto $(node)/image.tar.gz
	@docker load -i $(node)/image.tar.gz
