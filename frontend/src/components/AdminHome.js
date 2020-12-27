import { Button, Row, Col } from 'antd';
import '../css/AdminHome.css';

const AdminHome = () => (
    <div className="admin-home-div">
        <Row gutter={24}>
            <Col span={8}>
                <Button type="primary" className="admin-home-btn" onClick={event =>  window.location.href='/sales'} style={{background: "#12cc18", borderColor: "#12cc18"}}>SALES</Button>
            </Col>
            <Col span={8}>
                <Button type="primary" className="admin-home-btn" onClick={event =>  window.location.href='/purchaseorders'}>PURCHASES</Button>
            </Col>
            <Col span={8}>
                <Button type="primary" className="admin-home-btn" onClick={event =>  window.location.href='/waste'} danger>WASTE</Button>
            </Col>
        </Row>
    </div>
);

export default AdminHome;