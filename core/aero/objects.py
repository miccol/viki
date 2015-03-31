"""Describes the different objects used as abstraction of the AeroWorks configuration and modules."""
import helpers


class Interface:
    """An *interface* represents an in- or output of a module. This in- and outputs can be connected to other module's in- and outputs."""
    def __init__(self, interface_type,
                 name, message_type, required, link=None):
        #: Represents the name of the interface. E.g.: "cmd_vel"
        self.name = name
        #: Represents the type of the interface. E.g.: "ros_topic"
        self.type = interface_type
        #: Represents the message type the interface can handle. E.g.: "twist" or "standard_msgs/Empty"
        self.message_type = helpers.lookupMessageType(message_type)
        #: Defines if the interface is required to be connected. Execution will halt if this requirement is not met.
        self.required = required
        #: Contains the reference to the executable within the module that actually provides the in- or output. E.g.: "test_node/test_topic"
        self.link = link


class Internal_Interface:
    """An *internal_interface* represents a connection between an in- and output **within** a module. At this point, implicitly only implemented for *ros_topic* type interfaces.

    .. note:: In the future, this might be a specific case of :class:`Interface`.
    """
    def __init__(self, publisher, listener):
        #: Refers to the topic on which messages are be published. E.g. "node_name/command_giver"
        self.publisher = publisher
        #: Refers to the topic where the node is listening for messages. This topic is remapped to listen to the publisher. E.g. "node2_name/i_listen_here"
        self.listener = listener


class Module:
    """A *module* represents a separately distributable piece of software, that is able to work within the AeroWorks infrastructure.
    """
    def __init__(self, type, id):
        #: A list of :class:`Interface` describing all inputs of the module.
        self.inputs = []
        #: A list of :class:`Interface` describing all outputs of the module.
        self.outputs = []
        #: A list of :class:`Executable` describing all executables (ROS nodes) in the module.
        self.executables = []
        #: Represents the ID of the module, as defined in the ``module.xml``. This is used for identifying and selecting the module throughout the process, so this value should be unique.
        self.id = id
        #: Represents the type of the module, as defined in the ``module.xml``. This categorization is added for the comfort of the user. Examples are "userinput", "sensor", "controller" and "vehicle".
        self.type = type
        #: Contains a dictionary with all module metadata, as defined in ``module.xml``.
        self.meta = {}
        #: A list of :class:`Internal_Interface` describing all internal connections.
        self.config = []

    def addMeta(self, key, value):
        """Adds metadata to :attr:`meta`.

        :param key: The key of the metadata. E.g. "name"
        :type key: string
        :param value: The value of the metadata. E.g. "AeroWorks"
        :type value: string
        """
        self.meta[key] = value

    def addInput(self, interface):
        """Adds an input to the list of module inputs (:attr:`inputs`).

        :param interface: The interface to add
        :type interface: :class:`Interface`
        """
        self.inputs.append(interface)

    def addOutput(self, interface):
        """Adds an output to the list of module outputs (:attr:`outputs`).

        :param interface: The interface to add
        :type interface: :class:`Interface`
        """
        self.outputs.append(interface)

    def addExecutable(self, executable):
        """Adds an executable to the list of module executables (:attr:`executables`). Those executables are ROS nodes.

        :param executable: The executable to add.
        :type executable: :class:`Executable`
        """
        self.executables.append(executable)

    def addIntConnect(self, internal_interface):
        """Adds an internal connection to the list of module internal connections (:attr:`config`).

        :param internal_interface: The connection to add
        :type interface: :class:`Internal_Interface`
        """
        self.config.append(internal_interface)


class Executable:
    """An *executable* represents a ROS node that can be launched through a ROS launch file, generated by the AeroWorks infrastructure."""
    def __init__(self, id, pkg, executable):
        #: A list of :class:`Interface` describing all inputs of the executable.
        self.inputs = []
        #: A list of :class:`Interface` describing all outputs of the executable.
        self.outputs = []
        #: A list of :class:`Parameter` describing parameters to be set for the executable.
        self.params = []
        #: The ID of the executable, as given in the ``module.xml``.
        self.id = id
        #: The ROS package that contains the executable. E.g.: "joy"
        self.pkg = pkg
        #: The ROS node executable to launch. E.g. "joy_node".
        self.executable = executable

    def addInput(self, interface):
        """Adds an input to the list of executable inputs (:attr:`inputs`).

        :param interface: The interface to add
        :type interface: :class:`Interface`
        """
        self.inputs.append(interface)

    def addOutput(self, interface):
        """Adds an output to the list of executable outputs (:attr:`outputs`).

        :param interface: The interface to add
        :type interface: :class:`Interface`
        """
        self.outputs.append(interface)

    def addParameter(self, parameter):
        """Adds a parameter to the list of executable parameters (:attr:`params`).

        :param parameter: The parameter to add
        :type parameter: :class:`Parameter`
        """
        self.params.append(parameter)


class Parameter:
    def __init__(self, name, type, default=None, value=None):
        self.name = name
        self.default = default
        self.type = type
        self.value = value


class Configuration:
    def __init__(self, id):
        self.id = id
        self.modules_to_add = []
        self.connections_to_add = []
        self.namespaces = []


class Namespace:
    def __init__(self, id):
        self.id = id
        self.modules_to_add = []
        self.connections_to_add = []
        self.namespaces = []


class Module_to_add:
    def __init__(self, role, type, id, supress_warning=False):
        self.role = role
        self.id = id
        self.type = type
        self.supress_warning = supress_warning
        self.parameters_to_add = []

        # here we put Module classes used for implementation
        self.implementation = None


class Connection_to_add:
    def __init__(self, publisher, listener):
        self.publisher = publisher
        self.listener = listener


class Parameter_to_add:
    def __init__(self, name, value):
        self.name = name
        self.value = value
