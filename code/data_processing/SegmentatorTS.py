def segmentate_ts(ts_to_segmentate, number_of_segments):
    """
    Split ts on 'number_of_segments' approximately equal sized parts
    Inputs:
     ts_to_segmentate
     number_of_segments

    Outputs:
     segments           - list of data related to different segments
    """
    length_of_one_part = round(ts_to_segmentate.shape[0] / number_of_segments)
    segments = [ts_to_segmentate[round(part):round(part+length_of_one_part)] for part in range(0, ts_to_segmentate.shape[0], length_of_one_part)]

    return segments
