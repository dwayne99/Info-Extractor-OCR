import React, { Component } from 'react';
import {Button, Form, FormGroup, Label, FormText, Input} from "reactstrap";
import FileBase64 from 'react-file-base64';

import "./uploader.css";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faInfoCircle } from '@fortawesome/free-solid-svg-icons'

class Uploader extends Component {
    state = {  
        confirmation:"",
        isLoading : "",
        files :"",
        PAN:"",
        name:"",
        dob:"",
    }
    async handleSubmit(event){
        event.preventDefault();
        this.setState({confirmation:"Uploading the document..."});
    }

    async getFiles(files){
        this.setState({
            isLoading:"Extracting the data",
            files:files
        });

        const UID = Math.round(1+Math.random() * (100000-5));
        alert(UID);
        var data = {
            fileExt:"png",
            imageID: UID,
            folder: UID,
            img: this.state.files[0].base64
        };

        await fetch("https://2vdoldu1ma.execute-api.ap-south-1.amazonaws.com/Production",{
            method: "POST",
            headers:{
                Accept:"application/json",
                "content-Type":"application/json",
            },
            body:JSON.stringify(data)
        });
    }

    render() {
        const processing = "Please wait while the document is being processed..";
        return ( 
            <div className="row">
                <div className="col-6 offset-3">
                    <Form onSubmit={this.handleSubmit}>
                        <FormGroup>
                            <h3 className="text-danger">{processing}</h3>
                            <h6>Upload PAN card</h6>
                            <FormText color="muted">PNG,JPG,JPEG</FormText>
                            <div className="form-group files color">
                                <FileBase64 multiple={true} onDone={this.getFiles.bind(this)}></FileBase64>
                            </div>
                        </FormGroup>
                        <FormGroup>
                            <Label><h6>Permanent Account Number</h6></Label>
                            <Input type="text" name="pan" id="pan" required value={this.state.PAN}/>
                        </FormGroup>
                        <FormGroup>
                            <Label><h6>Name</h6></Label>
                            <Input type="text" name="name" id="name" required value={this.state.name}/>
                        </FormGroup>
                        <FormGroup>
                            <Label><h6>Date of Birth</h6></Label>
                            <Input type="text" name="dob" id="dob" required value={this.state.dob}/>
                        </FormGroup>
                        <Button className="btn btn-lg btn-block btn-success">Submit</Button>
                    </Form>
                </div>
            </div>
        );
    }
}

export default Uploader;