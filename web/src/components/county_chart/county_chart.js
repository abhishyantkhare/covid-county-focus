import React, { useEffect, useState } from 'react'
import DataChart from "../data_chart/data_chart"

const CountyChart = (props) => {

    const data_url_prefix = `${process.env.REACT_APP_BACKEND}/${props.state}`
    // Feb 1
    const startMs = 1580544000000
    // March 18
    const midMs = 1584514800000
    // May 1
    const endMs = 1588316400000
    const [cases, setCases] = useState([])
    const [deaths, setDeaths] = useState([])
    const [bedCapacityData, setBedCapacityData] = useState({})
    const [bedCapacity, setBedCapacity] = useState()


    useEffect(() => {
        checkAndFetchData()
    }, [props.county, props.state])
    const checkAndFetchData = () => {
        if (props.county.length == 0) {
            setCases([])
            setDeaths([])
            setBedCapacityData([])
            setBedCapacity()
            return
        }
        fetchCountyCases()
        fetchCountyDeaths()
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
                displayCases.push({
                    x: endMs,
                })

                setCases(displayCases)
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
                displayDeaths.push({
                    x: endMs,
                })

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

    return (
        <DataChart
            cases={cases}
            deaths={deaths}
            showBedCapacity={true}
            bedCapacityData={bedCapacityData}
            bedCapacity={bedCapacity}
            startMs={startMs}
            endMs={endMs} />
    )
}

export default CountyChart;