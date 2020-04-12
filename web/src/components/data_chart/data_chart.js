import React, { useEffect } from 'react'
import "./chart.css"
import Chart from 'chart.js';

const DataChart = (props) => {
    const cases = props.cases
    const deaths = props.deaths
    const projectedCases = props.projectedCases
    const bedCapacityData = props.bedCapacityData

    useEffect(() => {
        var ctx = document.getElementById('chart');
        var myLineChart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [
                    {
                        label: 'Cases',
                        data: cases,
                        fill: false,
                        borderColor: [
                            'rgba(46, 204, 113, 1)',
                        ],
                        borderWidth: 1,
                    },
                    {
                        label: 'Total Bed Capacity',
                        data: props.bedCapacityData,
                        fill: false,
                        borderColor: [
                            'rgba(155, 89, 182, 1)',
                        ],
                        borderWidth: 1,
                    },
                    {
                        label: 'Deaths',
                        data: deaths,
                        fill: false,
                        borderColor: [
                            'rgba(231, 76, 60, 1)',
                        ],
                        borderWidth: 1,
                    },
                    {
                        label: 'Projected Cases',
                        data: projectedCases,
                        fill: false,
                        borderColor: [
                            'rgba(52, 152, 219, 1)'
                        ],
                        borderWidth: 1,
                        borderDash: [10, 5]
                    }
                ]
            },
            options: {
                maintainAspectRatio: false,
                tooltips: {
                    intersect: false,
                },
                hover: {
                    intersect: false,
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }],
                    xAxes: [{
                        type: 'time',
                        time: {
                            unit: 'day',
                        },
                        ticks: {
                            beginAtZero: false
                        }
                    }]
                }
            }
        });
        return function cleanup() {
            myLineChart.destroy()
        }
    }, [cases, deaths, bedCapacityData, projectedCases])

    return (
        <div class='chart-container'>
            <canvas id="chart" />
        </div>
    )
}

export default DataChart;