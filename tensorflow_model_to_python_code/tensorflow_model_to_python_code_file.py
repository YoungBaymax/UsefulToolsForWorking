#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf # version 2.0.0
from tensorflow.keras.layers import  InputLayer, Conv1D, Conv2D, Dropout, MaxPooling1D, MaxPooling2D, AveragePooling1D, AveragePooling2D, GlobalMaxPooling1D, GlobalAveragePooling1D, BatchNormalization, concatenate, Permute, Flatten, Activation, UpSampling1D#,Input
from tensorflow.keras import Model, Input
try:
    import tensorflow.python.keras as keras
except:
    import tensorflow.keras as keras
import json
import os

class TF_Model():
    def __init__(self, model_path = None):
        self.model_path =model_path
        self.model_json_data = self.read_model_json_data()
        self.model_mode = self.model_json_data["class_name"]  # model in keras are "Model" or "Sequential"


    def read_model_json_data(self):
        with open(self.model_path, "r") as reader:
            json_data = json.load(reader)
            self._check_model(json_data)
            return json_data

    def _check_model(self, json_data):
        try:
            tf.keras.models.model_from_config(json_data)
        except:
            print("the model form json file is not a tensorflow model.")
            raise Exception("Sorry, tensorflow model is error")

    def get_function_body_from_Model(self) :
        # 是否有inputs，使用sequence与否，需要单独判断，此处节约时间，从Input出发还原模型
        config = self.model_json_data['config']
        class_name = self.model_json_data['class_name']
        model_name = config['name']
        layers = config['layers']

        body = ""
        # write input layer and middle layers
        for layer in layers :
            layer_name = layer['name']
            layer_class_name = layer['class_name']
            if layer_class_name == "InputLayer" :
                layer_class_name = "Input"
            layer_configs = layer['config']
            layer_inbound_nodes = layer['inbound_nodes']

            layer_head_string = layer_name + ' = ' + layer_class_name
            layer_configs_string = self.get_each_layer_configs(layer_configs = layer_configs)
            layer_inbound_string = self.get_each_layer_inbound_nodes(layer_inbound_nodes = layer_inbound_nodes)

            body += '\t'
            body += layer_head_string
            body += layer_configs_string
            body += layer_inbound_string
            body += '\n\n'

        # write model layer
        model_code_inputs = config['input_layers'][0][0]
        model_code_outputs = config['output_layers'][0][0]
        model_code_name = model_name
        body += '\t'
        body += "model = Model(inputs = {}, outputs = {}, name = \'{}\') \n\n".format(model_code_inputs,
                                                                                      model_code_outputs,
                                                                                      model_code_name)
        body += "\treturn model\n\n"

        return body

    def get_function_body_from_Sequencial(self) :
        # 是否有inputs，使用sequence与否，需要单独判断，此处节约时间，从Input出发还原模型
        config = self.model_json_data['config']
        class_name = self.model_json_data['class_name']
        model_name = config['name']
        body = "\tmodel = tf.keras.Sequential(name = \"{}\")\n".format(model_name)

        layers = config['layers']
        # write input layer and middle layers
        for layer in layers :
            # layer_name = layer['name']  #squence 中此处没有，name在config中
            layer_class_name = layer['class_name']
            # if layer_class_name == "InputLayer" :
            #     layer_class_name = "Input"
            layer_configs = layer['config']
            # layer_inbound_nodes = layer['inbound_nodes']

            layer_head_string = "model.add" + "(" + layer_class_name
            layer_configs_string = self.get_each_layer_configs(layer_configs = layer_configs)
            # layer_inbound_string = get_each_layer_inbound_nodes(layer_inbound_nodes = layer_inbound_nodes)

            body += '\t'
            body += layer_head_string
            # body += "model.add"
            body += layer_configs_string
            # body += layer_inbound_string
            body += ")"
            body += '\n\n'

            # writer.write('\t')
            # writer.write(head_string)
            # writer.write(configs_string)
            # writer.write(inbound_string)
            # writer.write('\n')

        # write model layer
        # model_code_inputs = config['input_layers'][0][0]
        # model_code_outputs = config['output_layers'][0][0]
        # model_code_name = model_name
        # body += '\t'
        # body += "model = Model(inputs = {}, outputs = {}, name = \'{}\') \n\n".format(model_code_inputs, model_code_outputs, model_code_name)
        body += "\treturn model\n\n"

        return body

    def get_each_layer_configs(self, layer_configs) :  # mode = Model or Sequential
        configs_string = '('

        for each_key in layer_configs.keys() :
            each_value = layer_configs[each_key]

            # --------------initializer中有(configs)
            # if each_key in ["kernel_initializer", "bias_initializer"] :
            if "initializer" in each_key :
                initializer_name = each_value['class_name']
                initializer_configs = each_value['config']
                each_value = initializer_name + '('
                for initializer_config_key in initializer_configs.keys() :
                    initializer_config_value = initializer_configs[initializer_config_key]
                    # if initializer_config in ['mode', 'distribution']:
                    # layer_config_value = "{}{} = \"{}\",".format(layer_config_value, initializer_config, initializer_configs[initializer_config])
                    # if type(initializer_config_value) == type("stringtype") :
                    if isinstance(initializer_config_value, str) :
                        each_value = "{}{} = \"{}\", ".format(each_value, initializer_config_key,
                                                              initializer_config_value)
                    else :
                        each_value = "{}{} = {}, ".format(each_value, initializer_config_key, initializer_config_value)
                each_value += ')'

            # --------------each_value为字符串时，需要加双引号  ""
            # elif type(each_value) == type("stringtype"):
            elif isinstance(each_value, str) :
                each_value = "\"{}\"".format(each_value)
            elif each_key == 'batch_input_shape' :
                each_key = "shape"
                each_value = each_value[1 :]
                if self.model_mode == "Model" and layer_configs["name"] != "InputLayer" :
                    each_key = "input_shape"
                # pass
                # 可以在D:\Program Files\Anaconda3\Lib\site-packages\tensorflow_core\python\keras\engine中更改了#加入了如下代码：
                #  if 'batch_input_shape' in kwargs:
                # batch_input_shape = kwargs.pop('batch_input_shape')
                # batch_size = batch_input_shape[0]
                # shape = batch_input_shape[1 :]
            configs_string = "{}{} = {}, ".format(configs_string, each_key, each_value)

        configs_string += ')'

        return configs_string

    def get_each_layer_inbound_nodes(self, layer_inbound_nodes) :
        if layer_inbound_nodes != [] :
            layer_code_inbound = '('
            for node_indx in range(len(layer_inbound_nodes[0])) :
                layer_code_inbound += layer_inbound_nodes[0][node_indx][0]
                if node_indx < len(layer_inbound_nodes[0]) - 1 :
                    layer_code_inbound += ", "
            layer_code_inbound += ')'
            if len(layer_inbound_nodes[0]) > 1 :
                layer_code_inbound = layer_code_inbound.replace('(', '([').replace(')', '])')
        else :
            layer_code_inbound = '\n'
        return layer_code_inbound

    def write_python_file(self, save_path = "tensorflow---model.py") :
        if not save_path.endswith(".py"):
            save_path = save_path + ".py"
        writer = open(save_path, 'w')
        writer.write("import tensorflow as tf\n")
        writer.write("from tensorflow.keras.layers import *\n")
        writer.write("from tensorflow.keras import *\n")
        writer.write("from tensorflow.keras.initializers import *\n")
        writer.write("from tensorflow import float32\n")

        writer.write("def build_model():\n")
        if self.model_mode == "Sequential" :
            writer.write(self.get_function_body_from_Sequencial())
        if self.model_mode == "Model":
            writer.write(self.get_function_body_from_Model())
        writer.close()

if __name__ == "__main__":

    def model_Sequence(input_length, nChannels) :
        # inputs = Input((input_length, nChannels), name = "input_layer")
        model = tf.keras.Sequential()
        model.add(Conv1D(16, 32, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal',
                         input_shape = (input_length, nChannels)))
        model.add(Conv1D(16, 32, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal'))
        model.add(MaxPooling1D(pool_size = 2))
        model.add(tf.keras.layers.AveragePooling1D(pool_size = 2, strides = 2, padding = "SAME"))
        model.summary()
        return model

    def model_Model(input_length, nChannels) :
        inputs = Input((input_length, nChannels), name = "input_layer")
        conv1 = Conv1D(16, 32, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal',
                       input_shape = (input_length, nChannels))(inputs)
        conv2 = Conv1D(16, 32, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal',
                       input_shape = (input_length, nChannels))(conv1)
        outs = tf.keras.layers.AveragePooling1D(pool_size = 2, strides = 2, padding = "SAME")(conv2)
        model = Model(inputs, outs)
        model.summary()
        return model

    def test_for_Sequence_model():
        model = model_Sequence(1280, 12)
        model_string = model.to_json()
        model_save_path = "model_Sequential.json"
        with open(model_save_path, 'w') as writer :
            writer.write(model_string)
        model_converter = TF_Model(model_path = model_save_path)
        model_converter.write_python_file(model_save_path)


    def test_for_Model_model() :
        model = model_Model(1280, 12)
        model_string = model.to_json()
        model_save_path = "model_Model.json"
        with open(model_save_path, 'w') as writer :
            writer.write(model_string)
        model_converter = TF_Model(model_path = model_save_path)
        model_converter.write_python_file(model_save_path)


    test_for_Sequence_model()
    test_for_Model_model()