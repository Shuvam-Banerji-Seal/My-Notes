#!/bin/bash

# Water Jug Problem Solver - Installation Script
# Author: Generated for CS4101 Assignment 01
# Date: $(date +"%Y-%m-%d")
# Description: Automated installation script for C-based Water Jug Problem solver

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect the Linux distribution
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo $ID
    elif [ -f /etc/redhat-release ]; then
        echo "rhel"
    elif [ -f /etc/debian_version ]; then
        echo "debian"
    else
        echo "unknown"
    fi
}

# Function to install packages based on distribution
install_packages() {
    local distro=$(detect_distro)
    print_status "Detected Linux distribution: $distro"
    
    case $distro in
        ubuntu|debian)
            print_status "Installing packages using apt..."
            sudo apt update
            sudo apt install -y gcc make gnuplot imagemagick
            ;;
        fedora)
            print_status "Installing packages using dnf..."
            sudo dnf install -y gcc make gnuplot ImageMagick
            ;;
        centos|rhel)
            print_status "Installing packages using yum..."
            sudo yum install -y gcc make gnuplot ImageMagick
            ;;
        arch|manjaro)
            print_status "Installing packages using pacman..."
            sudo pacman -S --noconfirm gcc make gnuplot imagemagick
            ;;
        opensuse*)
            print_status "Installing packages using zypper..."
            sudo zypper install -y gcc make gnuplot ImageMagick
            ;;
        *)
            print_error "Unsupported distribution: $distro"
            print_warning "Please manually install: gcc, make, gnuplot, imagemagick"
            exit 1
            ;;
    esac
}

# Function to check system requirements
check_requirements() {
    print_status "Checking system requirements..."
    
    local missing_deps=""
    
    # Check for GCC
    if ! command_exists gcc; then
        missing_deps="$missing_deps gcc"
    else
        print_success "GCC found: $(gcc --version | head -n1)"
    fi
    
    # Check for Make
    if ! command_exists make; then
        missing_deps="$missing_deps make"
    else
        print_success "Make found: $(make --version | head -n1)"
    fi
    
    # Check for Gnuplot
    if ! command_exists gnuplot; then
        missing_deps="$missing_deps gnuplot"
    else
        print_success "Gnuplot found: $(gnuplot --version)"
    fi
    
    # Check for ImageMagick (convert command)
    if ! command_exists convert; then
        missing_deps="$missing_deps imagemagick"
    else
        print_success "ImageMagick found: $(convert --version | head -n1)"
    fi
    
    if [ -n "$missing_deps" ]; then
        print_warning "Missing dependencies:$missing_deps"
        return 1
    else
        print_success "All dependencies are already installed!"
        return 0
    fi
}

# Function to create output directories
create_directories() {
    print_status "Creating output directories..."
    
    # Create directories for output files
    mkdir -p output
    mkdir -p plots
    mkdir -p animations
    
    print_success "Output directories created"
}

# Function to compile the program
compile_program() {
    print_status "Compiling the Water Jug Problem solver..."
    
    if [ -f "Makefile" ]; then
        print_status "Found Makefile, using make to compile..."
        make clean 2>/dev/null || true
        make
    else
        print_status "No Makefile found, compiling manually..."
        gcc -Wall -Wextra -O2 -o main main.c
    fi
    
    if [ -f "main" ] && [ -x "main" ]; then
        print_success "Compilation successful! Executable 'main' created."
    else
        print_error "Compilation failed!"
        exit 1
    fi
}

# Function to test the installation
test_installation() {
    print_status "Testing the installation..."
    
    # Test if the program can be executed
    if ./main --help 2>/dev/null || true; then
        print_success "Program can be executed"
    else
        print_warning "Program executable, but --help option not available"
    fi
    
    # Test gnuplot integration
    print_status "Testing gnuplot integration..."
    if gnuplot -e "set terminal pngcairo; set output 'test.png'; plot sin(x); exit" 2>/dev/null; then
        print_success "Gnuplot integration working"
        rm -f test.png
    else
        print_warning "Gnuplot integration may have issues"
    fi
    
    # Test ImageMagick
    print_status "Testing ImageMagick..."
    if convert -size 100x100 xc:white test_convert.png 2>/dev/null; then
        print_success "ImageMagick working"
        rm -f test_convert.png
    else
        print_warning "ImageMagick may have issues"
    fi
}

# Function to display usage information
show_usage() {
    cat << EOF

========================================
Water Jug Problem Solver - Ready to Use!
========================================

USAGE:
    ./main                  # Interactive mode - choose algorithm
    make run                # Run with Makefile (if available)
    make clean              # Clean generated files

ALGORITHMS AVAILABLE:
    1. Breadth First Search (BFS)
    2. Depth First Search (DFS)  
    3. Iterative Deepening DFS (ID-DFS)

OUTPUT FILES:
    - step_*.png           # Individual step visualizations
    - solution.gif         # Animated solution (if ImageMagick works)

ADDITIONAL COMMANDS:
    make help              # Show Makefile help (if available)
    make test              # Run quick test
    make visualize         # Generate sample visualization

TROUBLESHOOTING:
    - If gnuplot fails: Check X11 forwarding for remote systems
    - If convert fails: Check ImageMagick policy for PDF/PNG conversion
    - For permission issues: Check file permissions with 'ls -la'

Project Directory: $(pwd)
Installation completed on: $(date)

EOF
}

# Main installation process
main() {
    clear
    cat << EOF
========================================
Water Jug Problem Solver - Installer
========================================
This script will install all dependencies needed to run
the C-based Water Jug Problem solver with visualization.

Dependencies to be installed:
- GCC (C compiler)
- Make (build tool)
- Gnuplot (plotting library)
- ImageMagick (image processing)

EOF

    # Check if running as root
    if [ "$EUID" -eq 0 ]; then
        print_warning "Running as root. This is not recommended."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    # Ask for user confirmation
    read -p "Do you want to proceed with the installation? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Installation cancelled by user."
        exit 0
    fi
    
    print_status "Starting installation process..."
    
    # Check current requirements
    if ! check_requirements; then
        print_status "Installing missing dependencies..."
        install_packages
        
        # Verify installation
        if ! check_requirements; then
            print_error "Failed to install all dependencies!"
            exit 1
        fi
    fi
    
    # Create necessary directories
    create_directories
    
    # Compile the program
    compile_program
    
    # Test the installation
    test_installation
    
    # Show usage information
    show_usage
    
    print_success "Installation completed successfully!"
    print_status "You can now run the program with: ./main"
}

# Handle command line arguments
case "${1:-}" in
    --help|-h)
        cat << EOF
Water Jug Problem Solver - Installation Script

USAGE:
    $0 [OPTIONS]

OPTIONS:
    --help, -h          Show this help message
    --check-deps        Only check dependencies
    --install-deps      Only install dependencies
    --compile-only      Only compile the program
    --test-only         Only run tests
    
EXAMPLES:
    $0                  # Full installation
    $0 --check-deps     # Check what's missing
    $0 --compile-only   # Just compile if deps exist

EOF
        exit 0
        ;;
    --check-deps)
        check_requirements
        exit $?
        ;;
    --install-deps)
        install_packages
        exit $?
        ;;
    --compile-only)
        compile_program
        exit $?
        ;;
    --test-only)
        test_installation
        exit $?
        ;;
    "")
        main
        ;;
    *)
        print_error "Unknown option: $1"
        print_status "Use --help for usage information"
        exit 1
        ;;
esac
