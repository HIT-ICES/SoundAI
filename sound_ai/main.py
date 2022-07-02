import time
import ffmpeg
import pickle
import os
import sys
import numpy
import librosa
import librosa.core
import librosa.feature
import yaml
from sklearn import metrics
from keras.models import Model
from keras.layers import Input, Dense

app = Flask(__name__)
@app.route('/soundai/detect', methods=['POST'])
def detect():
    if request.method == 'POST':
        data_json = json.loads(request.data.decode('utf-8'))
        if 'path' in data_json:
            path = data_json['path']  # type: str

    (

    ffmpeg

    .input('rtsp://' + HOST, allowed_media_types='audio',t=10)['a']   # allowed_media_types='audio' 只读取音频流 t=10 只读取十秒（因为数据集里事分成了十秒一段）

    .output('./resources/saved_audio.wav', acodec='pcm_s16le', ac=1, ar='16k')

    .overwrite_output()

    .run(capture_stdout=True)

    )
    with open("baseline.yaml") as stream:
        param = yaml.safe_load(stream)
    model = keras_model(param["feature"]["n_mels"] * param["feature"]["frames"])
    model.summary()
    model_file ='./model/model_valve_id_00_6dB.hdf5'
    if os.path.exists(model_file):
        model.load_weights(model_file)

    data = file_to_vector_array('./dataset/saved_audio.wav',
                                n_mels=param["feature"]["n_mels"],
                                frames=param["feature"]["frames"],
                                n_fft=param["feature"]["n_fft"],
                                hop_length=param["feature"]["hop_length"],
                                power=param["feature"]["power"])

    error = numpy.mean(numpy.square(data - model.predict(data)), axis=1)#axis = 1: 压缩列，对各行求均值，返回m*1的矩阵
    y_pred = numpy.mean(error)
    if(y_pred>10):
        req='abnormal'
        return jsonify({"result": req})
    else:
        req='normal'
        return jsonify({"result": req})

    return jsonify({"code": 1})


########################################################################
# keras model
########################################################################
def keras_model(inputDim):
    """
    define the keras model
    the model based on the simple dense auto encoder (64*64*8*64*64)
    """
    inputLayer = Input(shape=(inputDim,))
    h = Dense(64, activation="relu")(inputLayer)
    h = Dense(64, activation="relu")(h)
    h = Dense(8, activation="relu")(h)
    h = Dense(64, activation="relu")(h)
    h = Dense(64, activation="relu")(h)
    h = Dense(inputDim, activation=None)(h)

    return Model(inputs=inputLayer, outputs=h)


########################################################################

# wav file Input
def file_load(wav_name, mono=False):
    """
    load .wav file.
    wav_name : str
        target .wav file
    sampling_rate : int
        audio file sampling_rate
    mono : boolean
        When load a multi channels file and this param True, the returned data will be merged for mono data
    return : numpy.array( float )
    """
    try:
        return librosa.load(wav_name, sr=None, mono=mono)
    except Exception as e:
        import traceback
        traceback.print_exc()
def demux_wav(wav_name, channel=0):
    """
    demux .wav file.
    wav_name : str
        target .wav file
    channel : int
        target channel number
    return : numpy.array( float )
        demuxed mono data
    Enabled to read multiple sampling rates.
    Enabled even one channel.
    """
    try:
        multi_channel_data, sr = file_load(wav_name)
        if multi_channel_data.ndim <= 1:
            return sr, multi_channel_data

        return sr, numpy.array(multi_channel_data)[channel, :]

    except ValueError as msg:
        print(msg)
########################################################################
# feature extractor
########################################################################
def file_to_vector_array(file_name,
                         n_mels=64,
                         frames=5,
                         n_fft=1024,
                         hop_length=512,
                         power=2.0):
    """
    convert file_name to a vector array.
    file_name : str
        target .wav file
    return : numpy.array( numpy.array( float ) )
        vector array
        * dataset.shape = (dataset_size, fearture_vector_length)
    """
    # 01 calculate the number of dimensions
    dims = n_mels * frames

    # 02 generate melspectrogram using librosa (**kwargs == param["librosa"])
    sr, y = demux_wav(file_name)
    mel_spectrogram = librosa.feature.melspectrogram(y=y,
                                                     sr=sr,
                                                     n_fft=n_fft,
                                                     hop_length=hop_length,
                                                     n_mels=n_mels,
                                                     power=power)

    # 03 convert melspectrogram to log mel energy
    log_mel_spectrogram = 20.0 / power * numpy.log10(mel_spectrogram + sys.float_info.epsilon)

    # 04 calculate total vector size
    vectorarray_size = len(log_mel_spectrogram[0, :]) - frames + 1

    # 05 skip too short clips
    if vectorarray_size < 1:
        return numpy.empty((0, dims), float)

    # 06 generate feature vectors by concatenating multi_frames
    vectorarray = numpy.zeros((vectorarray_size, dims), float)
    for t in range(frames):
        vectorarray[:, n_mels * t: n_mels * (t + 1)] = log_mel_spectrogram[:, t: t + vectorarray_size].T

    return vectorarray


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)