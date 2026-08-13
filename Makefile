CC = gcc

CFLAGS  = -std=gnu11 -Wall -Wextra -O3 -I. -Iinclude
LDFLAGS = -lasound -lpthread -lm

OBJ = .obj
BUILD = build

SRCS = $(wildcard src/*.c) $(wildcard lib/*.c)
OBJS = $(patsubst %.c, $(OBJ)/%.o, $(notdir $(SRCS)))

vpath %.c src lib

APP_NAME = qgpuApp
APP = $(BUILD)/$(APP_NAME)

all: prepare $(APP)

prepare:
	@mkdir -p $(OBJ) $(BUILD)

$(OBJ)/%.o: %.c
	@echo "Compilation $<..."
	@$(CC) $(CFLAGS) -c $< -o $@

$(APP): $(OBJS)
	@echo "Linking app $(APP)..."
	@$(CC) -o $@ $(OBJS) $(LDFLAGS)

run: all
	@clear && ./$(BUILD)/$(APP_NAME)

clean:
	@echo "Cleaning..."
	@rm -rf $(OBJ) $(BUILD)
	@echo "Cleaned!"

.PHONY: all prepare run clean
