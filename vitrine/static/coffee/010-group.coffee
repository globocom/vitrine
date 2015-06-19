# This file is part of vitrine.
# https://github.com/globocom/vitrine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Globo.com <talentos@corp.globo.com>

plotSkillSet = (placeholder, data) ->
  $.plot placeholder, data,
    grid: borderWidth: 0
    series: bars:
      show: true
      barWidth: 0.5
      align: 'center'
      fill: 1
    xaxis:
      mode: 'categories'
      tickLength: 0
      font:
        size: 12
        family: 'HelveticaNeue, Arial, sans-serif'
        color: '#474D57'
    yaxis:
      show: false
      tickLength: 0

commits2Stackbars = (data) ->
  projects = {}
  for year of data
    for month of data[year]
      item = year + '/' + month
      for proj of data[year][month]
        if !projects[proj]
          projects[proj] = []
        projects[proj].push [
          item
          data[year][month][proj]
        ]
  chartData = Object.keys(projects).map((key) ->
    projects[key]
  )
  chartData

plotCommitsChart = (placeholder, data) ->
  # Require: jquery.flot.stack, jquery.flot.categories
  $.plot placeholder, commits2Stackbars(data),
    series:
      stack: 0
      bars:
        fill: 1.0
        show: true
        barWidth: 0.6
        lineWidth: 0
    colors: [
      '#4A8DE5'
      '#F7A807'
      '#B6EB83'
      '#D25461'
    ]
    xaxis:
      mode: 'categories'
      tickLength: 0
    grid:
      borderWidth: 0
      aboveData: true
      markings: [
        {
          color: '#E5E5E5'
          lineWidth: 1
          xaxis:
            from: 4
            to: 4
        }
        {
          color: '#E5E5E5'
          lineWidth: 1
          xaxis:
            from: 8
            to: 8
        }
      ]
  return

plotSkillSet('#placeholder', d5)
plotCommitsChart('#activity_placeholder', commits)
