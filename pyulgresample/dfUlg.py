"""Create dataframe from .ulg file and convert it to other structures.

Read required topics. 
Create ulog structure from .ulg file. 
Create pandas dataframe

"""
from abc import ABCMeta, abstractmethod
import os
from pyulgresample import loginfo
from pyulgresample import ulogconv as conv


class TopicMsgs:
    """Store topic messages."""

    def __init__(self, topic, msgs):
        """Initialization.
        
        Arguments:
        topic -- topic that is used to generate df and ulog
        msgs -- messages from that topics

        """
        self.topic = topic
        self.msgs = msgs


class dfUlgBase(metaclass=ABCMeta):
    """Base class, converts .ulg file into ulog-structure and pandas-dataframe.

    Check .ulg file.
    Read required topics. 
    Create new data structures.

    Keyword arguments:
    metaclass -- (default ABCMeta)

    """

    def __init__(self, df, ulog, topics):
        """Initialization.
        
        Arguments:
        df -- pandas dataframe with uORB msgs from topics 
        ulog -- pyulog struct of uORB msgs (without resampling)
        topics -- list of topics that are used to generate df and ulog

        """
        self.df = df  # pandas dataframe
        self.ulog = ulog  # ulog
        self.topics = topics  # PX4-uorb topics

    @classmethod
    def _check_file(self, filepath):
        """Check if file is a .ulg file.

        Arguments:
            filepat -- path to .ulg-file

        """
        if os.path.isfile(filepath):
            base, ext = os.path.splitext(filepath)
            if ext.lower() not in (".ulg"):
                raise Exception("File is not .ulg file")
        else:
            raise Exception("File does not exist")

    @classmethod
    def create(
        cls, filepath, additional_topics=None, additional_zoh_topics=None
    ):
        """Factory method. Create a dfulgBase object.

        By default, the merge-method uses linear interpolation for resampling.
        Dataframe (df) is a pandas-dataframe with index equal to the merged timestamps. Each column represents a message-field.
        For instance, the thrust-field of the message vehicle_local_position_setpoint message would be named as follow:
            T_vehicle_local_position_setpoint_0__F_thrust_x
        if the field x of vehicle_local_position_setpoint is a scalar or
            T_vehicle_local_position_setpoint_0__F_x_0
        if the field x is an array, where the 0 represents the index of the array.
        The T stands for topic, which indicates the beginning of the topic. In this example, the topcic name is vehicle_local_position_setpoint.
        The topic name is followed by a number, which indicates the topic instance. If there is only one instance of a specific topic, then this number will be 0.
        The instance number is followed by two underlines and a capital letter F, which stands for field. In the example above, the field in question is x.

        Arguments:
        filepath -- path to .ulg file

        Keyword arguments:
        additional_topics -- topics from which pandas-dataframe and ulog-struct are constructed (default None)
        additional_zoh_topics -- topics which are resampled through zero order hold (default None)

        """
        # bind argument to new name such that they are not overwritten by accident
        topics = additional_topics
        zoh_topics = additional_zoh_topics

        # check if valid file is provided
        cls._check_file(filepath)

        # Add required topics to topics if not already present
        if topics is not None:
            topics.extend(
                x for x in cls.get_required_topics() if x not in topics
            )
        else:
            topics = cls.get_required_topics()

        ulog = loginfo.get_ulog(filepath, topics)

        # Add required zoh-topics if not already present
        if zoh_topics is not None:
            zoh = zoh_topics.extend(
                x for x in cls.get_required_zoh_topics() if x not in zoh_topics
            )
        else:
            zoh = cls.get_required_zoh_topics()

        if ulog is None:
            raise Exception("Ulog is empty")

        pandadict = conv.createPandaDict(ulog, cls.get_nan_topic_msgs())
        df = conv.merge(pandadict, zoh, cls.get_nan_topic_msgs())
        # change to seconds
        df.timestamp = (df.timestamp - df.timestamp[0]) * 1e-6
        return cls(df, ulog, topics)

    @classmethod
    @abstractmethod
    def get_required_topics(self):
        """Abstract method, get required topics."""
        return []

    @classmethod
    @abstractmethod
    def get_required_zoh_topics(self):
        """Abstract method, get the topics on which zero order hold resampling is applied."""
        return []

    @classmethod
    @abstractmethod
    def get_nan_topic_msgs(self):
        """Abstract method, get a list of messages which contain NAN-information and return.

        An example topic is vehicle_local_position_setpoint, where the position msg x/y/z can contain
        NAN-values, which indicates that this particular message was not used in the control loop.

        """
        return []
