const nodemailer = require('nodemailer');
const fs = require('fs');

const transporter = nodemailer.createTransport({
  host: 'smtp.qq.com',
  port: 587,
  secure: false,
  auth: {
    user: '878155028@qq.com',
    pass: 'htphtehvbhrjbahh'
  }
});

const mailOptions = {
  from: '878155028@qq.com',
  to: 'account35.szx@bestservices.com.cn',
  subject: '科目余额表_结果.xlsx',
  text: '科目余额表月度往来对账结果，请查收附件。',
  attachments: [
    {
      filename: '科目余额表_结果.xlsx',
      path: '/home/leonwan/.openclaw/workspace/科目余额表_结果.xlsx'
    }
  ]
};

transporter.sendMail(mailOptions, (error, info) => {
  if (error) {
    console.log('Error:', error.message);
  } else {
    console.log('Email sent:', info.response);
  }
});
