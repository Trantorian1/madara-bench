# ============================================================================ #
#                         STARKNET NODE BENCHMAR RUNNER                        #
# ============================================================================ #

NODES := madara
IMGS := $(addsuffix /image.tar.gz,$(NODES))

RESET    := \033[0m
ACCENT   := \033[1;36m   # bold cyan
TERTIARY := \033[2;3;37m # dim white italic

.PHONY: all
all: help

.PHONY: help
help:
	@echo "TODO(help)"

.PHONY: run
run: images
	@for node in $(NODES); do \
		docker-compose -f $$node/compose.yaml up; \
	done

.PHONY: images
images: $(IMGS)

.PHONY: clean
clean:
	@echo -e "$(TERTIARY)stopping all containers$(RESET)"
	@for node in $(NODES); do \
		docker-compose -f $$node/compose.yaml stop; \
	done
	@echo -e "$(TERTIARY)removing all images$(RESET)"
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
	@echo -e "$(TERTIARY)building$(RESET) $(ACCENT)$(node)$(RESET)" ;
	@nix-build $(node) -o $(node)/result
	@$(node)/result/bin/copyto $(node)/image.tar.gz
	@docker load -i $(node)/image.tar.gz
