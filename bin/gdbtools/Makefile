DEST = ~/.gdb

install: EastlStdContainers.o gdb_stl_utils gdb_tls_utils gdb_checkstack_utils
	@mkdir -p $(DEST)
	cp EastlStdContainers.o $(DEST)/EastlStdContainers.o
	sed -e 's!__DEST__!$(DEST)!' gdb_stl_utils >$(DEST)/gdb_stl_utils
	cp gdb_tls_utils $(DEST)/gdb_tls_utils
	chmod 644 $(DEST)/gdb_tls_utils
	cp gdb_checkstack_utils $(DEST)/gdb_checkstack_utils
	chmod 644 $(DEST)/gdb_checkstack_utils
	cp gdb_fiber_utils $(DEST)/gdb_fiber_utils
	chmod 644 $(DEST)/gdb_fiber_utils
	cp gdb_log_dump $(DEST)/gdb_log_dump
	chmod 644 $(DEST)/gdb_log_dump
	@echo ""
	@echo "Done. You may want to add the following line to your ~/.gdbinit:"
	@echo "         source $(DEST)/gdb_stl_utils"
	@echo "         source $(DEST)/gdb_tls_utils"
	@echo "         source $(DEST)/gdb_checkstack_utils"
	@echo "         source $(DEST)/gdb_fiber_utils"
	@echo "         source $(DEST)/gdb_log_dump"

clean:
	rm -f EastlStdContainers.o

uninstall:
	rm -f $(DEST)/EastlStdContainers.o
	rm -f $(DEST)/gdb_stl_utils
	rm -f $(DEST)/gdb_tls_utils
	rm -f $(DEST)/gdb_checkstack_utils
	rm -f $(DEST)/gdb_fiber_utils
	rm -f $(DEST)/gdb_log_dump

EastlStdContainers.o: EastlStdContainers.cpp
	g++ -I../../external/eabase/include/Common -I../../external/eastl/include -Wall -g -o $@ -c $<

.PHONY: install
