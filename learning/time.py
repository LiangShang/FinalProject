__author__ = 'Sherlock'


def parse_time(time_string):
    """Given the time_string like the
    '__init__.py\n
     command.py\n
     main.py\n
     time.py\n
     \n
     real\t0m0.002s\n
     user\t0m0.001s\n
     sys\t0m0.001s'
    """
    times = time_string.split("\n")

    user_time_str = times[-2].split("\t")[-1]
    sys_time_str = times[-1].split("\t")[-1]

    #print user_time_str, sys_time_str

    user_time = parse_m_s(user_time_str)
    sys_time = parse_m_s(sys_time_str)

    return user_time + sys_time


def parse_m_s(m_s_str):

    minute, second = m_s_str.split("m")
    second = second[0:-1]
    #print minute, second

    return float(second) + float(minute)*60


if __name__ == "__main__":
    parse_time("__init__.py\ncommand.py\nmain.py\ntime.py\n\nreal\t0m0.002s\nuser\t0m0.001s\nsys\t0m0.001s")
