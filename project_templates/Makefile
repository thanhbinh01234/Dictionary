#
# Makefile
#
#
#

###########################

# You need to edit these values.

DICT_NAME		=	"My Dictionary"
DICT_SRC_PATH		=	MyDictionary.xml
CSS_PATH		=	MyDictionary.css
PLIST_PATH		=	MyInfo.plist

DICT_BUILD_OPTS		=
# Suppress adding supplementary key.
# DICT_BUILD_OPTS		=	-s 0	# Suppress adding supplementary key.

###########################

# The DICT_BUILD_TOOL_DIR value is used also in "build_dict.sh" script.
# You need to set it when you invoke the script directly.

DICT_BUILD_TOOL_DIR	=	$(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
DICT_BUILD_TOOL_BIN	=	$(DICT_BUILD_TOOL_DIR)/../bin



###########################

DICT_DEV_KIT_OBJ_DIR	=	$(DICT_BUILD_TOOL_DIR)/objects
export	DICT_DEV_KIT_OBJ_DIR

DESTINATION_FOLDER	=	$(DICT_BUILD_TOOL_DIR)/Dictionary
RM			=	/bin/rm

###########################

all:
	@echo $(DICT_DEV_KIT_OBJ_DIR)
	@mkdir -p $(DICT_DEV_KIT_OBJ_DIR)
	@echo "$(DICT_BUILD_TOOL_BIN)"
	@"$(DICT_BUILD_TOOL_BIN)/build_dict.sh" $(DICT_BUILD_OPTS) $(DICT_NAME) $(DICT_SRC_PATH) $(CSS_PATH) $(PLIST_PATH)
	@echo "Done."


# install:
# 	echo "Installing into $(DESTINATION_FOLDER)".
# 	mkdir -p $(DESTINATION_FOLDER)
# 	cp $(DICT_DEV_KIT_OBJ_DIR)/$(DICT_NAME).dictionary  $(DESTINATION_FOLDER)/$(DICT_NAME).dictionary
# 	touch $(DESTINATION_FOLDER)
# 	echo "Done."
# 	echo "To test the new dictionary, try Dictionary.app."

# clean:
# 	$(RM) -rf $(DICT_DEV_KIT_OBJ_DIR)
