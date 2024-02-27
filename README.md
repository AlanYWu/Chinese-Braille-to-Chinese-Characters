# Vision Braille
 This research used Bi-LSTM to infer the tone from tone-omitted Chinese phonetics.


The Webapp demonstration is in "0_Webapp-braille-vision"


Vision Braille Project: Bridging Education for Blind Children

# Introduction

In China, approximately 240,000 children between the ages of 0 and 17 face visual disabilities. Unfortunately, their educational opportunities remain limited to a handful of specialized schools. These schools often struggle to find qualified braille teachers, making education for blind students a challenging endeavor.

Recognizing this gap, I embarked on the Vision Braille Project. The project aims to empower blind children by providing an innovative solution: a braille translation website. This platform facilitates communication between traditional schoolteachers and visually impaired students. 

How It Works:

- Input Braille Text: Teachers upload written homework or assignments in braille to the website.
- Instant Translation: The website swiftly translates the braille content into standard text (pinyin or Chinese characters).
- Accessible Learning: Teachers can now understand and evaluate the work of blind students, fostering inclusive education.
By bridging this gap, the Vision Braille Project ensures that blind children can learn alongside their sighted peers, unlocking a brighter future for all. 🌟



The tesing app is available at **[Vision Braille Project](http://154.12.37.165:5000/)**




# Flow Chart


![alt text](braille-vision-flowchart_new.png)

# Method

## Long Short-Term Memory (LSTM) Networks
To address the limitations of traditional Recurrent Neural Networks (such as gradient vanishing and exploding), we adopt LSTM (Long Short-Term Memory) networks. LSTMs enhance RNNs by introducing three essential components:

Forget Gate:
Prevents gradient explosion and vanishing by selectively retaining relevant historical information.
Allows the model to forget irrelevant past states.

Memory Cell:
Maintains a memory of previous historical information.
Captures long-term dependencies.

Output Gate:
Integrates memory information to produce the final output.
Enables the LSTM to capture long-distance computational relationships.

![alt text](image.png)

LSTM Network Architecture; LSTM Structure Figure 3: Illustration of LSTM Structure

Update Equations for Input Data at Time t

$\begin{matrix}\mathbf{i}_t&=\sigma(\mathbit{W}_i\mathbf{h}_{t-1}+\mathbit{U}_i\mathbf{x}_t+\mathbit{b}_i)\\\mathbf{f}_t&=\sigma(\mathbit{W}_f\mathbf{h}_{t-1}+\mathbit{U}_f\mathbf{x}_t+\mathbit{b}_f)\\{\buildrel\mathbf{c}\over\mathbf{c}~}_t&=\tanh\funcapply(\mathbit{W}_c\mathbf{h}_{t-1}+\mathbit{U}_c\mathbf{x}_t+\mathbit{b}_c)\\\mathbf{c}_t&=\mathbf{f}_t\odot\mathbf{c}_{t-1}+\mathbf{i}_t\odot{\buildrel\mathbf{c}\over\mathbf{c}~}_t\\\mathbf{o}_t&=\sigma(\mathbit{W}_o\mathbf{h}_{t-1}+\mathbit{U}_o\mathbf{x}_t+\mathbit{b}_o)\\\mathbf{h}_t&=\mathbf{o}_t\odot\tanh\funcapply(\mathbf{c}_t)\\\end{matrix}$

Where:
$\sigma$ represents the sigmoid function.
$\odot$ denotes element-wise multiplication.
$x_t$ is the input vector at time $t$, which in our case is the word-embedded input vector.
$h_t$ represents the hidden state, incorporating all previous states up to time $t$.
$U$ and $W$ are the weights and biases for each layer.


# Results



# Contributors




