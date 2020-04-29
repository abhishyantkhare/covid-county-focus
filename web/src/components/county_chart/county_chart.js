import React, { useEffect, useState } from 'react'
import DataChart from "../data_chart/data_chart"

const CountyChart = (props) => {

    const data_url_prefix = `${process.env.REACT_APP_BACKEND}/${props.state}`
    // Feb 1
    const DEFAULT_START_MS = 1580544000000
    // Current time
    const DEFAULT_END_MS = Date.now()
    // Midway
    const DEFAULT_MID_MS = Math.floor((DEFAULT_END_MS + DEFAULT_START_MS) / 2)

    const [cases, setCases] = useState([])
    const [deaths, setDeaths] = useState([])
    const [startMs, setStartMs] = useState(DEFAULT_START_MS)
    const [midMs, setMidMs] = useState(DEFAULT_MID_MS)
    const [endMs, setEndMs] = useState(DEFAULT_END_MS)
    const [projectedCases, setProjectedCases] = useState([])
    const [bedCapacityData, setBedCapacityData] = useState([])
    const [bedCapacity, setBedCapacity] = useState(0)


    useEffect(() => {
        fetchCaseAndDeaths()
    }, [props.county, props.state])

    // fetch deaths
    useEffect(() => {
        fetchBedCapacity()
    }, [props.county, props.state, cases])

    const fetchCaseAndDeaths = () => {
        if (props.county.length === 0) {
            setCases([])
            setDeaths([])
            return
        }
        fetchCountyCases()
        fetchCountyDeaths()
    }

    const fetchBedCapacity = () => {
        if (props.county.length === 0) {
            setBedCapacityData([])
            setBedCapacity(0)
            return
        }
        fetchCountyBedCapacity()
    }
    const fetchCountyCases = () => {
        const data_url = `${data_url_prefix}/${props.county}/cases`
        fetch(data_url)
            .then((response) => {
                return response.json()
            })
            .then((rawCases) => {
                const displayCases = rawCases.map(d => {
                    return {
                        x: d.epoch_ms,
                        y: d.cases,
                    }
                })
                setStartMs(displayCases[0].x)
                setMidMs(displayCases[Math.floor(rawCases.length / 2)].x)
                setEndMs(displayCases[displayCases.length - 1].x)
                /*   displayCases.push({
                       x: endMs,
                   })*/

                setCases(displayCases)
                fetchCountyBedCapacity()
            })
    }

    const fetchCountyDeaths = () => {
        const data_url = `${data_url_prefix}/${props.county}/deaths`
        fetch(data_url)
            .then((response) => {
                return response.json()
            })
            .then((rawDeaths) => {
                const displayDeaths = rawDeaths.map(d => {
                    return {
                        x: d.epoch_ms,
                        y: d.deaths,
                    }
                })
                /*   displayDeaths.push({
                       x: endMs,
                   })*/

                setDeaths(displayDeaths)
            })

    }

    const fetchCountyBedCapacity = () => {
        const data_url = `${data_url_prefix}/${props.county}/bed_capacity`
        fetch(data_url)
            .then((response) => {
                return response.json()
            })
            .then((bed_capacity_data) => {
                const capacity = bed_capacity_data['total_bed_capacity']
                const bedCapacityData = [
                    {
                        x: startMs,
                        y: capacity
                    },
                    {
                        x: midMs,
                        y: capacity
                    },
                    {
                        x: endMs,
                        y: capacity
                    }
                ]
                setBedCapacityData(bedCapacityData)
                setBedCapacity(capacity)
            })
    }

    const fetchCountyCaseProjections = () => {
        const data_url = `${data_url_prefix}/${props.county}/case_projections`
        fetch(data_url)
            .then((response) => {
                return response.json()
            })
            .then((rawProjectedCases) => {
                const displayProjectedCases = rawProjectedCases.map(d => {
                    return {
                        x: d.epoch_ms,
                        y: d.projected_cases,
                    }
                })
                /*  displayProjectedCases.push({
                      x: endMs,
                  })*/

                setProjectedCases(displayProjectedCases)
                console.log(displayProjectedCases)
            })
    }

    return (
        <DataChart
            cases={cases}
            deaths={deaths}
            projectedCases={projectedCases}
            showBedCapacity={true}
            bedCapacityData={bedCapacityData}
            bedCapacity={bedCapacity}
        />
    )
}

export default CountyChart;