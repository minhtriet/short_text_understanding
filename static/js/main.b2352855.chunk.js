(this.webpackJsonpshort_text_understand=this.webpackJsonpshort_text_understand||[]).push([[0],{14:function(e,t,n){},8:function(e,t,n){e.exports=n(9)},9:function(e,t,n){"use strict";n.r(t);var a=n(2),r=n(3),u=n(1),c=n(5),o=n(4),i=n(0),l=n.n(i),s=n(7),h=n.n(s),d=(n(14),function(e){Object(c.a)(n,e);var t=Object(o.a)(n);function n(e){var r;return Object(a.a)(this,n),(r=t.call(this,e)).state={query:""},r.handleChange=r.handleChange.bind(Object(u.a)(r)),r.handleSubmit=r.handleSubmit.bind(Object(u.a)(r)),r}return Object(r.a)(n,[{key:"handleSubmit",value:function(e){fetch("/api/v1?query=".concat(encodeURIComponent(this.state.query))).then((function(e){return e.json()})).then((function(e){console.log(e)}),(function(e){console.log(e)})),e.preventDefault()}},{key:"handleChange",value:function(e){this.setState({query:e.target.value})}},{key:"render",value:function(){return l.a.createElement("form",{onSubmit:this.handleSubmit,method:"GET"},l.a.createElement("div",{id:"textbox_container"},l.a.createElement("input",{id:"textbox_query",value:this.state.query,onChange:this.handleChange,type:"text"})))}}]),n}(l.a.Component)),m=function(e){Object(c.a)(n,e);var t=Object(o.a)(n);function n(){return Object(a.a)(this,n),t.apply(this,arguments)}return Object(r.a)(n,[{key:"render",value:function(){return l.a.createElement("div",null,l.a.createElement(d,null),l.a.createElement("div",{className:"result"}),l.a.createElement("mark",null," Jack ")," is cool")}}]),n}(l.a.Component);h.a.render(l.a.createElement(m,null),document.getElementById("root"))}},[[8,1,2]]]);
//# sourceMappingURL=main.b2352855.chunk.js.map