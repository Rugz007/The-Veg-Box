import { useEffect, useState } from 'react'
import axios from 'axios';
import { Spin, Select, Col, Row, Input, Button, Radio, message } from "antd";
import '../css/Sales.css';

var loading = true;
const { Option } = Select;
var oldInput = [];
var newInput = [];
var oldInputJSON = null;
var newInputJSON = null;

const Sales = () => {
    const [data, setData] = useState([]);
    const [inputList, setInputList] = useState([{ id: "", item_name:"", rate: "", quantity: "", discounted_rate: "", subtotal:"", item_unit: "" }]);
    const [total, setTotal] = useState(0);
    const [name, setName] = useState("");
    const [phone, setPhone] = useState("");
    const [payment, setPayment] = useState("CASH");
    const [orderID, setOrderID] = useState(0);

    useEffect(() => {
        axios.get(`http://0.0.0.0:8000/api/items/`,
            {
                headers:
                {
                    'Content-Type': 'application/json'
                }
            }).then((res) => {
                loading = false;
                setData(res.data.results);
            }).catch((err) => {
                alert(err);
            });
        
    }, []);

    const handleSelectedItem = (e, index) => {
        const list = [...inputList];
        list[index]["id"] = data[e-1].id
        list[index]["rate"] = data[e-1].rate;
        list[index]["item_name"] = data[e-1].item_name;
        list[index]["item_unit"] = data[e-1].unit;
        list[index]["discounted_rate"] = "";
        list[index]["subtotal"] = "";
        list[index]["quantity"] = "";
        setInputList(list);
    }

    const handleAddClick = () => {
        setInputList([...inputList, { id: "", item_name:"", rate: "", quantity: "", discounted_rate: "", subtotal:"", item_unit: "" }]);
    };

    const handleNewBillClick = () => {
        setInputList([{ id: "", item_name:"", rate: "", quantity: "", discounted_rate: "", subtotal:"", item_unit: "" }]);
        setTotal(0);
        setPhone("");
        setName("");
        setOrderID(0);
        setPayment("CASH");
    };

    const handlePrintClick = () => {
        var index = 0;
        const regex =  /^\d+(\.\d{0,2})?$/;
        while (index < inputList.length) { 
            if (inputList[index].item_name === "")
                return alert("Error! Empty row not allowed!");
            if (inputList[index].quantity === "")
                return alert("Error! Quantity not specified!");
            if (!regex.test(inputList[index].quantity))
                return alert("Error! Quantity is invalid!");
            if (!regex.test(inputList[index].discounted_rate) && inputList[index].discounted_rate !== "")
                return alert("Error! Discounted Rate is invalid!");
            index++; 
        }
        if (orderID === 0)
        {
            var order = {
                biller: 1,
                customer_name: name, 
                customer_phone: phone,
                total: total,
                mode_of_payment: payment
            }
            var orderJSON = JSON.stringify(order);
            try {
                axios.post(`http://0.0.0.0:8000/api/sales/addorder/`,
                            orderJSON,
                            {
                                headers:
                                {
                                    'Content-Type': 'application/json'
                                }
                            }
                            ).then((response)=>{
                                setOrderID(response.data.id);
                                var orderItems = [];
                                var tempDict = {
                                    quantity: "",
                                    item_rate: "",
                                    discounted_rate: "",
                                    order: "",
                                    item: ""
                                };
                                var index = 0
                                while (index < inputList.length) { 
                                    if (inputList[index].discounted_rate === "")
                                        tempDict = {
                                            quantity: inputList[index].quantity,
                                            item_rate: inputList[index].rate,
                                            discounted_rate: 0,
                                            order: response.data.id,
                                            item: inputList[index].id
                                        };
                                    else
                                        tempDict = {
                                            quantity: inputList[index].quantity,
                                            item_rate: inputList[index].rate,
                                            discounted_rate: inputList[index].discounted_rate,
                                            order: response.data.id,
                                            item: inputList[index].id
                                        };
                                    orderItems.push(tempDict);
                                    index++; 
                                }
                                var orderItemsJSON = JSON.stringify(orderItems);
                                try {
                                    axios.post(`http://0.0.0.0:8000/api/sales/addorderitems/`,
                                            orderItemsJSON,
                                            {
                                                headers:
                                                {
                                                    'Content-Type': 'application/json'
                                                }
                                            }
                                    ).then((res)=>{
                                        message.success('Order Created Successfully!');
                                        var index = 0
                                        const list = [...inputList];
                                        while (index < list.length) { 
                                            oldInput.push(list[index]);
                                            index++; 
                                        }
                                        oldInputJSON = JSON.stringify(oldInput);
                                        window.open('http://0.0.0.0:8000/receipt/'+response.data.id+'/');
                                    });
                                } catch (error) {
                                    alert(error);
                                }
                            })
            } catch (error) {
                alert(error);
            }
        }
        else{
            index = 0;
            newInput = [];
            const list = [...inputList];
            while (index < list.length) { 
                newInput.push(list[index]);
                index++;
            }
            newInputJSON = JSON.stringify(newInput)
            if(newInputJSON === oldInputJSON)
            {
                window.open('http://0.0.0.0:8000/receipt/'+orderID+'/');
            }
            else
            {
                order = {
                    biller: 1,
                    customer_name: name, 
                    customer_phone: phone,
                    total: total,
                    mode_of_payment: payment
                }
                orderJSON = JSON.stringify(order);
                try{
                    axios.put(`http://0.0.0.0:8000/api/sales/updateorder/`+ orderID +`/`,
                        orderJSON,
                        {
                            headers:
                            {
                                'Content-Type': 'application/json'
                            }
                        }
                    );
                }catch (error) {
                    alert(error);
                }
                
                try {
                    axios.get(`http://0.0.0.0:8000/api/sales/deleteorderitems/`+ orderID +`/`,
                            {
                                headers:
                                {
                                    'Content-Type': 'application/json'
                                }
                            }
                    ).then((res)=>{
                        var orderItems = [];
                        var tempDict = {
                            quantity: "",
                            item_rate: "",
                            discounted_rate: "",
                            order: "",
                            item: ""
                        };
                        var index = 0
                        while (index < inputList.length) { 
                            if (inputList[index].discounted_rate === "")
                                tempDict = {
                                    quantity: inputList[index].quantity,
                                    item_rate: inputList[index].rate,
                                    discounted_rate: 0,
                                    order: orderID,
                                    item: inputList[index].id
                                };
                            else
                                tempDict = {
                                    quantity: inputList[index].quantity,
                                    item_rate: inputList[index].rate,
                                    discounted_rate: inputList[index].discounted_rate,
                                    order: orderID,
                                    item: inputList[index].id
                                };
                            orderItems.push(tempDict);
                            index++; 
                        }
                        var orderItemsJSON = JSON.stringify(orderItems);
                        console.log(orderItemsJSON);
                        try {
                            axios.post(`http://0.0.0.0:8000/api/sales/addorderitems/`,
                                    orderItemsJSON,
                                    {
                                        headers:
                                        {
                                            'Content-Type': 'application/json'
                                        }
                                    }
                            ).then((res)=>{
                                message.success('Order Updated Successfully!');
                                var index = 0
                                const list = [...inputList];
                                while (index < list.length) { 
                                    oldInput.push(list[index]);
                                    index++; 
                                }
                                oldInputJSON = JSON.stringify(oldInput);
                                window.open('http://0.0.0.0:8000/receipt/'+orderID+'/');
                            });
                        } catch (error) {
                            alert(error);
                        }
                    });
                } catch (error) {
                    alert(error);
                }

                
            }
        }
    };

    // handle input change
    const handleInputChange = (e, index) => {
        const regex = /^[\d.]+$/;
        
        if (e.target.value === "" || regex.test(e.target.value))
        {   
            const { name, value } = e.target;
            const list = [...inputList];
            if (e.target.value ==="." && list[index][name]==="")
                list[index][name] = "0.";
            else
                list[index][name] = value;
            if(list[index]["quantity"] !== "" && list[index]["rate"] !== "" && list[index]["discounted_rate"] === "")
                list[index]["subtotal"] = (list[index]["quantity"] * list[index]["rate"]).toFixed(2);
            if(list[index]["quantity"] !== "" && list[index]["rate"] !== "" && list[index]["discounted_rate"] !== "")
                list[index]["subtotal"] = (list[index]["quantity"] * list[index]["discounted_rate"]).toFixed(2);
            if(list[index]["quantity"] === "" && list[index]["discounted_rate"] === "")
                list[index]["subtotal"] = "";
            setInputList(list);
            setTotal(parseFloat((list.reduce((prev,next) => prev + parseFloat(next.subtotal),0)).toFixed(2)));
        }
    };

    // handle click event of the Remove button
    const handleRemoveClick = index => {
        const list = [...inputList];
        list.splice(index, 1);
        setInputList(list);
        setTotal(parseFloat((list.reduce((prev,next) => prev + parseFloat(next.subtotal),0)).toFixed(2)));
    };

    const handleNameChange = (e) => {
        var regex = /^[a-zA-Z ]*$/;
        if (e.target.value === "" || regex.test(e.target.value)) {
            setName(e.target.value);
        }
    }

    const handlePhoneChange = (e) => {
        const regex = /^[0-9\b]+$/;
        if (e.target.value === "" || regex.test(e.target.value)) {
            setPhone(e.target.value);
        }
    }

    const handlePaymentChange = (e) => {
        setPayment(e.target.value);
    }

    return (
        <div className="sales-div">
            <center></center>
            <Row gutter={12}>
                <Col span={6}>
                    <Button size="large" onClick={handleNewBillClick} style={{width:"100%", height: "50px"}} danger>New Receipt / Clear Fields</Button>
                </Col>
                <Col span={12}/>
                <Col span={6}>
                    <Button type="primary" size="large" onClick={handlePrintClick} style={{width:"100%", height: "50px"}} disabled={(inputList[0]["id"] !== "")? false:true}>Save and Print</Button>
                </Col>
            </Row>
            <br/>
            <br/>
            <br/>
            <Row gutter={24}>
                <Col span={8} style={{fontSize: "16px"}}>
                    <b>Customer Name</b>
                </Col>
                <Col span={6} style={{fontSize: "16px"}}>
                    <b>Phone Number</b>
                </Col>
                <Col span={5} style={{fontSize: "16px"}}>
                    <b>Payment Mode</b>
                </Col>
                <Col span={5} style={{fontSize: "16px"}}>
                    <b>Bill Number</b>
                </Col>
            </Row>
            <br/>
            <Row gutter={24}>
                <Col span={8}>
                    <Input placeholder="Customer Name" size="large" onChange={e => handleNameChange(e)} value={name} maxLength="100"/>
                </Col>
                <Col span={6}>
                    <Input placeholder="Phone Number" size="large" onChange={e => handlePhoneChange(e)} value={phone} maxLength="10"/>
                </Col>
                <Col span={5}>
                    <Radio.Group defaultValue="CASH" buttonStyle="solid" onChange={e => handlePaymentChange(e)} value={payment} size="large">
                        <Radio.Button value="CASH">Cash</Radio.Button>
                        <Radio.Button value="CARD">Card</Radio.Button>
                        <Radio.Button value="UPI">UPI</Radio.Button>
                    </Radio.Group>
                </Col>
                <Col span={5}>
                    <Input size="large" value={orderID} disabled/>
                </Col>
            </Row>
            <br/>
            <br/>
            <br/>
            <br/>
            <Row gutter={24}>
                <Col span={2}>
                </Col>
                <Col span={6} style={{fontSize: "16px"}}>
                    <b>Particulars</b>
                </Col>
                <Col span={4} style={{fontSize: "16px"}}>
                    <b>Quantity</b>
                </Col>
                <Col span={4} style={{fontSize: "16px"}}>
                    <b>Rate</b>
                </Col>
                <Col span={4} style={{fontSize: "16px"}}>
                    <b>Discounted Rate</b>
                </Col>
                <Col span={4} style={{fontSize: "16px"}}>
                    <b>Subtotal</b>
                </Col>
            </Row>
            <br/>
            {loading && <center><Spin /></center>}
            {
                !loading 
                &&
                inputList.map((x, i) => { 
                return (
                    <div>
                        <Row gutter={24}>
                            <Col span={2}>
                                {inputList.length !== 1 && <Button size="large" onClick={() => handleRemoveClick(i)} danger>Remove</Button>}
                            </Col>
                            <Col span={6}>
                                <Select
                                    showSearch
                                    placeholder="Select an item"
                                    optionFilterProp="children"
                                    size="large"
                                    style={{ width: 300 }}
                                    onSelect={e => handleSelectedItem(e, i)}
                                    value={x.item_name}
                                    name="id"
                                >
                                    <>
                                        {data.map((item) => (<Option key={item.id}>{item.item_name} </Option>))}
                                    </>
                                </Select>
                            </Col>
                            <Col span={4}>
                                <Input name="quantity" size="large" suffix={x.item_unit} value={x.quantity} onChange={e => handleInputChange(e, i)} disabled={!x.item_name}/>
                            </Col>
                            <Col span={4}>
                                <Input name="rate" size="large" prefix={(x.item_unit==="") ? "" : "₹"} suffix={(x.item_unit==="") ? "" : " / "+ x.item_unit} value={x.rate} onChange={e => handleInputChange(e, i)} disabled/>
                            </Col>
                            <Col span={4}>
                                <Input name="discounted_rate" placeholder= "Optional" size="large" prefix={(x.item_unit==="") ? "" : "₹"} suffix={(x.item_unit==="") ? "" : " / "+ x.item_unit} value={x.discounted_rate} onChange={e => handleInputChange(e, i)} disabled={!x.item_name}/>
                            </Col>
                            <Col span={4}>
                                <Input name="subtotal" size="large" prefix={(x.item_unit==="") ? "" : "₹"} value={x.subtotal} onChange={e => handleInputChange(e, i)} disabled/>
                            </Col>
                        </Row>
                        <br/>
                        <br/>
                        {inputList.length - 1 === i && <Button type="primary" size="large" onClick={handleAddClick} style={{width:"100%", background: "#12cc18", borderColor: "#12cc18", height: "50px"}}>Add</Button>}
                    </div>
                );})
            }
            <br/>
            <br/>
            <Row gutter={24}>
                <Col span={2}/>
                <Col span={6}/>
                <Col span={4}/>
                <Col span={4}/>
                <Col span={4} style={{textAlign: "right", fontSize: "30px"}}>
                    <b>Total</b>
                </Col>
                <Col span={4} style={{textAlign: "right", fontSize: "30px"}}>
                    <b> ₹ {total}</b>
                </Col>
            </Row>
            <br/>
        </div>
    );
}

export default Sales;





