# encoding: utf-8
def get_responsive_str(chart_id, width, height):
    return (
        "d3.select('#{} svg')".format(chart_id) +
          ".attr('viewBox', '0 0 {} {}')".format(width, height) +
          ".attr('preserveAspectRatio', 'xMinYMin meet')" +
          ".attr('width', '{}').attr('height', '{}')".format(width, height) +
          ".style('width', '100%').style('height', '100%')" +
          ";"
    )
