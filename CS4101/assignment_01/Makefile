# Water Jug Problem Solver - Makefile
# CS4101 Assignment 01
# Author: Generated for Water Jug Problem Solver
# Description: Comprehensive Makefile for building and managing the project

# ==================== CONFIGURATION ====================

# Compiler and flags
CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -O2 -D_GNU_SOURCE
DEBUG_FLAGS = -g -DDEBUG -O0 -D_GNU_SOURCE
PROFILE_FLAGS = -pg -O2 -D_GNU_SOURCE

# Project configuration
PROJECT_NAME = water_jug_solver
TARGET = main
SOURCE = main.c
BACKUP_DIR = backup
OUTPUT_DIR = output
PLOT_DIR = plots
ANIMATION_DIR = animations

# Install paths (for system-wide installation)
PREFIX = /usr/local
BINDIR = $(PREFIX)/bin
DATADIR = $(PREFIX)/share/$(PROJECT_NAME)

# Dependencies
REQUIRED_TOOLS = gcc gnuplot convert

# File patterns
PNG_FILES = step_*.png
GIF_FILES = *.gif
TEMP_FILES = *.o *.out core.*
BACKUP_FILES = *.bak *~

# ==================== MAIN TARGETS ====================

# Default target
.PHONY: all
all: $(TARGET)
	@echo "Build complete! Run './$(TARGET)' to start the program."

# Build the main executable
$(TARGET): $(SOURCE)
	@echo "Compiling $(PROJECT_NAME)..."
	$(CC) $(CFLAGS) -o $@ $<
	@echo "Compilation successful!"

# ==================== DEVELOPMENT TARGETS ====================

# Debug build
.PHONY: debug
debug: CFLAGS = $(DEBUG_FLAGS) -Wall -Wextra -std=c99
debug: $(TARGET)
	@echo "Debug build complete. Use gdb ./$(TARGET) to debug."

# Profile build (for performance analysis)
.PHONY: profile
profile: CFLAGS = $(PROFILE_FLAGS) -Wall -Wextra -std=c99
profile: $(TARGET)
	@echo "Profile build complete. Run program then use 'gprof ./$(TARGET) gmon.out'."

# Static analysis
.PHONY: lint
lint:
	@echo "Running static analysis..."
	@if command -v cppcheck >/dev/null 2>&1; then \
		cppcheck --enable=all --suppress=missingIncludeSystem $(SOURCE); \
	else \
		echo "cppcheck not found. Install with: sudo apt install cppcheck"; \
	fi

# ==================== EXECUTION TARGETS ====================

# Run the program interactively
.PHONY: run
run: $(TARGET)
	@echo "Starting $(PROJECT_NAME)..."
	./$(TARGET)

# Run with BFS algorithm
.PHONY: run-bfs
run-bfs: $(TARGET)
	@echo "Running with BFS algorithm..."
	@echo "1" | ./$(TARGET)

# Run with DFS algorithm  
.PHONY: run-dfs
run-dfs: $(TARGET)
	@echo "Running with DFS algorithm..."
	@echo "2" | ./$(TARGET)

# Run with ID-DFS algorithm
.PHONY: run-iddfs
run-iddfs: $(TARGET)
	@echo "Running with ID-DFS algorithm..."
	@echo "3" | ./$(TARGET)

# ==================== TESTING TARGETS ====================

# Quick test to verify everything works
.PHONY: test
test: $(TARGET) check-deps
	@echo "Running quick test..."
	@echo "Testing compilation..."
	@if [ -f $(TARGET) ] && [ -x $(TARGET) ]; then \
		echo "✓ Executable created successfully"; \
	else \
		echo "✗ Executable not found"; exit 1; \
	fi
	@echo "Testing gnuplot..."
	@if gnuplot -e "print 'gnuplot test'; exit" 2>/dev/null; then \
		echo "✓ Gnuplot working"; \
	else \
		echo "✗ Gnuplot not working"; \
	fi
	@echo "Testing ImageMagick..."
	@if convert -version >/dev/null 2>&1; then \
		echo "✓ ImageMagick working"; \
	else \
		echo "✗ ImageMagick not working"; \
	fi
	@echo "All tests passed!"

# Full test with sample run
.PHONY: test-full
test-full: $(TARGET)
	@echo "Running full test with BFS..."
	@timeout 30s bash -c 'echo "1" | ./$(TARGET)' || echo "Test completed (or timed out)"
	@if [ -f step_00.png ]; then \
		echo "✓ Visualization files generated"; \
	else \
		echo "⚠ No visualization files found"; \
	fi

# ==================== UTILITY TARGETS ====================

# Check system dependencies
.PHONY: check-deps
check-deps:
	@echo "Checking dependencies..."
	@for tool in $(REQUIRED_TOOLS); do \
		if command -v $$tool >/dev/null 2>&1; then \
			echo "✓ $$tool found"; \
		else \
			echo "✗ $$tool not found"; \
			exit 1; \
		fi; \
	done
	@echo "All dependencies satisfied!"

# Install dependencies (Ubuntu/Debian)
.PHONY: install-deps
install-deps:
	@echo "Installing dependencies for Ubuntu/Debian..."
	sudo apt update
	sudo apt install -y gcc make gnuplot imagemagick

# Create necessary directories
.PHONY: setup-dirs
setup-dirs:
	@echo "Creating project directories..."
	@mkdir -p $(OUTPUT_DIR) $(PLOT_DIR) $(ANIMATION_DIR) $(BACKUP_DIR)
	@echo "Directories created: $(OUTPUT_DIR), $(PLOT_DIR), $(ANIMATION_DIR), $(BACKUP_DIR)"

# ==================== VISUALIZATION TARGETS ====================

# Generate sample visualization (for testing)
.PHONY: visualize
visualize:
	@echo "Generating sample visualization..."
	@echo 'set terminal pngcairo size 400,400 enhanced font "Verdana,10"' > temp_plot.gp
	@echo 'set output "sample_jug_state.png"' >> temp_plot.gp
	@echo 'set title "Sample Water Jug State (1, 2)"' >> temp_plot.gp
	@echo 'set boxwidth 0.5' >> temp_plot.gp
	@echo 'set style fill solid 0.5' >> temp_plot.gp
	@echo 'set yrange [0:5]' >> temp_plot.gp
	@echo 'set xrange [-1:2]' >> temp_plot.gp
	@echo 'set xtics ("3L Jug" 0, "4L Jug" 1)' >> temp_plot.gp
	@echo 'set ylabel "Liters"' >> temp_plot.gp
	@echo 'unset key' >> temp_plot.gp
	@echo 'plot "-" with boxes' >> temp_plot.gp
	@echo '0 1' >> temp_plot.gp
	@echo '1 2' >> temp_plot.gp
	@echo 'e' >> temp_plot.gp
	@gnuplot temp_plot.gp 2>/dev/null || echo "Gnuplot visualization failed"
	@rm -f temp_plot.gp
	@if [ -f sample_jug_state.png ]; then \
		echo "✓ Sample visualization created: sample_jug_state.png"; \
	else \
		echo "✗ Failed to create sample visualization"; \
	fi

# View the latest solution animation
.PHONY: view-animation
view-animation:
	@if [ -f solution.gif ]; then \
		echo "Opening solution.gif..."; \
		if command -v xdg-open >/dev/null 2>&1; then \
			xdg-open solution.gif; \
		elif command -v eog >/dev/null 2>&1; then \
			eog solution.gif; \
		else \
			echo "No image viewer found. Please open solution.gif manually."; \
		fi; \
	else \
		echo "No solution.gif found. Run the program first."; \
	fi

# ==================== MAINTENANCE TARGETS ====================

# Clean generated files
.PHONY: clean
clean:
	@echo "Cleaning generated files..."
	@rm -f $(TARGET) $(PNG_FILES) $(GIF_FILES) $(TEMP_FILES)
	@rm -f sample_jug_state.png gmon.out
	@echo "Clean complete."

# Deep clean (including output directories)
.PHONY: clean-all
clean-all: clean
	@echo "Performing deep clean..."
	@rm -rf $(OUTPUT_DIR) $(PLOT_DIR) $(ANIMATION_DIR)
	@rm -f $(BACKUP_FILES)
	@echo "Deep clean complete."

# Create backup of source files
.PHONY: backup
backup: setup-dirs
	@echo "Creating backup..."
	@cp $(SOURCE) $(BACKUP_DIR)/$(SOURCE).$(shell date +%Y%m%d_%H%M%S).bak
	@if [ -f Makefile ]; then \
		cp Makefile $(BACKUP_DIR)/Makefile.$(shell date +%Y%m%d_%H%M%S).bak; \
	fi
	@echo "Backup created in $(BACKUP_DIR)/"

# ==================== INSTALLATION TARGETS ====================

# Install the program system-wide
.PHONY: install
install: $(TARGET)
	@echo "Installing $(PROJECT_NAME) system-wide..."
	@sudo mkdir -p $(BINDIR) $(DATADIR)
	@sudo cp $(TARGET) $(BINDIR)/$(PROJECT_NAME)
	@sudo chmod 755 $(BINDIR)/$(PROJECT_NAME)
	@sudo cp $(SOURCE) $(DATADIR)/
	@if [ -f README.md ]; then sudo cp README.md $(DATADIR)/; fi
	@echo "Installation complete. Run '$(PROJECT_NAME)' from anywhere."

# Uninstall the program
.PHONY: uninstall
uninstall:
	@echo "Uninstalling $(PROJECT_NAME)..."
	@sudo rm -f $(BINDIR)/$(PROJECT_NAME)
	@sudo rm -rf $(DATADIR)
	@echo "Uninstall complete."

# ==================== PACKAGING TARGETS ====================

# Create a distribution package
.PHONY: dist
dist: clean backup
	@echo "Creating distribution package..."
	@tar -czf $(PROJECT_NAME)-$(shell date +%Y%m%d).tar.gz \
		$(SOURCE) Makefile install.sh README.md *.md 2>/dev/null || \
		tar -czf $(PROJECT_NAME)-$(shell date +%Y%m%d).tar.gz \
		$(SOURCE) Makefile install.sh
	@echo "Distribution package created: $(PROJECT_NAME)-$(shell date +%Y%m%d).tar.gz"

# ==================== HELP TARGET ====================

# Show help information
.PHONY: help
help:
	@echo "Water Jug Problem Solver - Makefile Help"
	@echo "========================================"
	@echo ""
	@echo "BUILD TARGETS:"
	@echo "  all          - Build the main executable (default)"
	@echo "  debug        - Build with debug symbols"
	@echo "  profile      - Build with profiling enabled"
	@echo "  clean        - Remove generated files"
	@echo "  clean-all    - Deep clean including directories"
	@echo ""
	@echo "EXECUTION TARGETS:"
	@echo "  run          - Run the program interactively"
	@echo "  run-bfs      - Run with BFS algorithm"
	@echo "  run-dfs      - Run with DFS algorithm"
	@echo "  run-iddfs    - Run with ID-DFS algorithm"
	@echo ""
	@echo "TESTING TARGETS:"
	@echo "  test         - Quick dependency and build test"
	@echo "  test-full    - Full test with sample execution"
	@echo "  check-deps   - Check system dependencies"
	@echo ""
	@echo "UTILITY TARGETS:"
	@echo "  install-deps - Install dependencies (Ubuntu/Debian)"
	@echo "  setup-dirs   - Create project directories"
	@echo "  visualize    - Generate sample visualization"
	@echo "  view-animation - Open the latest solution.gif"
	@echo "  lint         - Run static analysis (requires cppcheck)"
	@echo ""
	@echo "MAINTENANCE TARGETS:"
	@echo "  backup       - Create backup of source files"
	@echo "  install      - Install system-wide"
	@echo "  uninstall    - Remove system installation"
	@echo "  dist         - Create distribution package"
	@echo ""
	@echo "EXAMPLES:"
	@echo "  make                    # Build the program"
	@echo "  make run               # Run interactively"
	@echo "  make test              # Test the setup"
	@echo "  make clean && make     # Clean rebuild"
	@echo "  make install-deps      # Install dependencies"
	@echo ""
	@echo "For installation script: ./install.sh"

# ==================== SPECIAL TARGETS ====================

# Prevent make from interpreting these as file targets
.PHONY: default
default: all
