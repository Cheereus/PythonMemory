#coding:utf-8
# 为智能计算考试查到的关于正向传递与反向传播的代码
import random
import math

#
#   参数解释：
#   "pd_" ：偏导的前缀
#   "d_" ：导数的前缀
#   "w_ho" ：隐含层到输出层的权重系数索引
#   "w_ih" ：输入层到隐含层的权重系数的索引

class NeuralNetwork:
    # 文中学习率为 0.5
    # LEARNING_RATE = 0.5
    # 卷中学习率为 0.8
    LEARNING_RATE = 0.8

    def __init__(self, num_inputs, num_hidden, num_outputs, hidden_layer_weights = None, hidden_layer_bias = None, output_layer_weights = None, output_layer_bias = None):
        self.num_inputs = num_inputs

        self.hidden_layer = NeuronLayer(num_hidden, hidden_layer_bias)
        self.output_layer = NeuronLayer(num_outputs, output_layer_bias)

        self.init_weights_from_inputs_to_hidden_layer_neurons(hidden_layer_weights)
        self.init_weights_from_hidden_layer_neurons_to_output_layer_neurons(output_layer_weights)

    def init_weights_from_inputs_to_hidden_layer_neurons(self, hidden_layer_weights):
        weight_num = 0
        for h in range(len(self.hidden_layer.neurons)):
            for i in range(self.num_inputs):
                if not hidden_layer_weights:
                    self.hidden_layer.neurons[h].weights.append(random.random())
                else:
                    self.hidden_layer.neurons[h].weights.append(hidden_layer_weights[weight_num])
                weight_num += 1

    def init_weights_from_hidden_layer_neurons_to_output_layer_neurons(self, output_layer_weights):
        weight_num = 0
        for o in range(len(self.output_layer.neurons)):
            for h in range(len(self.hidden_layer.neurons)):
                if not output_layer_weights:
                    self.output_layer.neurons[o].weights.append(random.random())
                else:
                    self.output_layer.neurons[o].weights.append(output_layer_weights[weight_num])
                weight_num += 1

    def inspect(self):
        print('------')
        print('* Inputs: {}'.format(self.num_inputs))
        print('------')
        print('Hidden Layer')
        self.hidden_layer.inspect()
        print('------')
        print('* Output Layer')
        self.output_layer.inspect()
        print('------')

    def feed_forward(self, inputs, isForward):
        hidden_layer_outputs = self.hidden_layer.feed_forward(inputs, isForward)
        return self.output_layer.feed_forward(hidden_layer_outputs, isForward)

    def train(self, training_inputs, training_outputs):
        self.feed_forward(training_inputs, True)

        # 1. 输出神经元的值
        #print('输出神经元的值')
        pd_errors_wrt_output_neuron_total_net_input = [0] * len(self.output_layer.neurons)
        for o in range(len(self.output_layer.neurons)):

            # ∂E/∂zⱼ
            pd_errors_wrt_output_neuron_total_net_input[o] = self.output_layer.neurons[o].calculate_pd_error_wrt_total_net_input(training_outputs[o])
            #print(pd_errors_wrt_output_neuron_total_net_input[o])

        # 2. 隐含层神经元的值
        #print('------')
        #print('隐含层神经元的值')
        pd_errors_wrt_hidden_neuron_total_net_input = [0] * len(self.hidden_layer.neurons)
        for h in range(len(self.hidden_layer.neurons)):

            # dE/dyⱼ = Σ ∂E/∂zⱼ * ∂z/∂yⱼ = Σ ∂E/∂zⱼ * wᵢⱼ
            d_error_wrt_hidden_neuron_output = 0
            for o in range(len(self.output_layer.neurons)):
                d_error_wrt_hidden_neuron_output += pd_errors_wrt_output_neuron_total_net_input[o] * self.output_layer.neurons[o].weights[h]

            # ∂E/∂zⱼ = dE/dyⱼ * ∂zⱼ/∂
            pd_errors_wrt_hidden_neuron_total_net_input[h] = d_error_wrt_hidden_neuron_output * self.hidden_layer.neurons[h].calculate_pd_total_net_input_wrt_input()
            #print(pd_errors_wrt_hidden_neuron_total_net_input[h])

        # 3. 更新输出层权重系数
        print('------')
        print('更新输出层权重系数')
        for o in range(len(self.output_layer.neurons)):
            for w_ho in range(len(self.output_layer.neurons[o].weights)):

                # ∂Eⱼ/∂wᵢⱼ = ∂E/∂zⱼ * ∂zⱼ/∂wᵢⱼ
                pd_error_wrt_weight = pd_errors_wrt_output_neuron_total_net_input[o] * self.output_layer.neurons[o].calculate_pd_total_net_input_wrt_weight(w_ho)

                # Δw = α * ∂Eⱼ/∂wᵢ
                self.output_layer.neurons[o].weights[w_ho] -= self.LEARNING_RATE * pd_error_wrt_weight
                print(self.output_layer.neurons[o].weights[w_ho])

        # 4. 更新隐含层的权重系数
        print('------')
        print('更新隐含层的权重系数')
        for h in range(len(self.hidden_layer.neurons)):
            for w_ih in range(len(self.hidden_layer.neurons[h].weights)):

                # ∂Eⱼ/∂wᵢ = ∂E/∂zⱼ * ∂zⱼ/∂wᵢ
                pd_error_wrt_weight = pd_errors_wrt_hidden_neuron_total_net_input[h] * self.hidden_layer.neurons[h].calculate_pd_total_net_input_wrt_weight(w_ih)

                # Δw = α * ∂Eⱼ/∂wᵢ
                self.hidden_layer.neurons[h].weights[w_ih] -= self.LEARNING_RATE * pd_error_wrt_weight
                print(self.hidden_layer.neurons[h].weights[w_ih])

    def calculate_total_error(self, training_sets):
        total_error = 0
        for t in range(len(training_sets)):
            training_inputs, training_outputs = training_sets[t]
            for o in range(len(training_outputs)):
                total_error += self.output_layer.neurons[o].calculate_error(training_outputs[o])
            self.feed_forward(training_inputs, False)
        print('总误差')
        print(total_error)
        return total_error

class NeuronLayer:
    def __init__(self, num_neurons, bias):

        # 同一层的神经元共享一个截距项b
        self.bias = bias if bias else random.random()

        self.neurons = []
        for i in range(num_neurons):
            self.neurons.append(Neuron(self.bias))

    def inspect(self):
        print('Neurons:', len(self.neurons))
        for n in range(len(self.neurons)):
            print(' Neuron', n)
            for w in range(len(self.neurons[n].weights)):
                print('  Weight:', self.neurons[n].weights[w])
            print('  Bias:', self.bias)

    def feed_forward(self, inputs, isForward):
        outputs = []
        for neuron in self.neurons:
            outputs.append(neuron.calculate_output(inputs, isForward))
        return outputs

    def get_outputs(self):
        outputs = []
        for neuron in self.neurons:
            outputs.append(neuron.output)
        return outputs

class Neuron:
    def __init__(self, bias):
        self.bias = bias
        self.weights = []

    def calculate_output(self, inputs, isForward):
        self.inputs = inputs
        self.output = self.squash(self.calculate_total_net_input(isForward))
        if isForward :
            print('计算神经元的输出：')
        if isForward :
            print(self.output)
        return self.output

    def calculate_total_net_input(self, isForward):
        if isForward :
            print('计算神经元的输入加权和：')
        total = 0
        for i in range(len(self.inputs)):
            total += self.inputs[i] * self.weights[i]
        if isForward :   
            print(total + self.bias)
        return total + self.bias
        

    # 激活函数sigmoid
    def squash(self, total_net_input):
        return 1 / (1 + math.exp(-total_net_input))


    def calculate_pd_error_wrt_total_net_input(self, target_output):
        return self.calculate_pd_error_wrt_output(target_output) * self.calculate_pd_total_net_input_wrt_input()

    # 每一个神经元的误差是由平方差公式计算的
    def calculate_error(self, target_output):
        print('------')
        print('每个输出神经元的误差')
        print(0.5 * (target_output - self.output) ** 2)
        return 0.5 * (target_output - self.output) ** 2

    
    def calculate_pd_error_wrt_output(self, target_output):
        return -(target_output - self.output)

    
    def calculate_pd_total_net_input_wrt_input(self):
        return self.output * (1 - self.output)


    def calculate_pd_total_net_input_wrt_weight(self, index):
        return self.inputs[index]


# 文中的例子:
# nn = NeuralNetwork(2, 2, 2, hidden_layer_weights=[0.15, 0.2, 0.25, 0.3], hidden_layer_bias=0.35, output_layer_weights=[0.4, 0.45, 0.5, 0.55], output_layer_bias=0.6)
# nn.inspect()
# for i in range(1):
#    nn.train([0.05, 0.1], [0.01, 0.99])
#    nn.calculate_total_error([[[0.05, 0.1], [0.01, 0.99]]])


# 卷子上的数据:

nn = NeuralNetwork(2, 2, 2, hidden_layer_weights=[0.2, 0.4, -0.3, 0.1], hidden_layer_bias=1, output_layer_weights=[0.35, 0.5, 0.4, 0.45], output_layer_bias=1)
nn.inspect()
for i in range(1):
    nn.train([1, 0], [0, 1])
    nn.calculate_total_error([[[1, 0], [0, 1]]])

# 参考自 https://www.cnblogs.com/charlotte77/p/5629865.html