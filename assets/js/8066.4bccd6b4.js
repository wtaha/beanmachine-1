"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[8066],{39960:function(e,n,t){t.r(n),t.d(n,{default:function(){return v}});var r=t(63366),o=t(67294),u=t(73727),i=t(52263),a=t(13919),c=t(10412),l=(0,o.createContext)({collectLink:function(){}}),s=t(44996),f=t(18780),d=["isNavLink","to","href","activeClassName","isActive","data-noBrokenLinkCheck","autoAddBaseUrl"];var v=function(e){var n,t,v=e.isNavLink,g=e.to,m=e.href,p=e.activeClassName,h=e.isActive,b=e["data-noBrokenLinkCheck"],w=e.autoAddBaseUrl,y=void 0===w||w,E=(0,r.Z)(e,d),P=(0,i.default)().siteConfig,C=P.trailingSlash,L=P.baseUrl,S=(0,s.useBaseUrlUtils)().withBaseUrl,D=(0,o.useContext)(l),A=g||m,k=(0,a.Z)(A),R=null==A?void 0:A.replace("pathname://",""),x=void 0!==R?(t=R,y&&function(e){return e.startsWith("/")}(t)?S(t):t):void 0;x&&k&&(x=(0,f.applyTrailingSlash)(x,{trailingSlash:C,baseUrl:L}));var T=(0,o.useRef)(!1),V=v?u.OL:u.rU,O=c.default.canUseIntersectionObserver,M=(0,o.useRef)();(0,o.useEffect)((function(){return!O&&k&&null!=x&&window.docusaurus.prefetch(x),function(){O&&M.current&&M.current.disconnect()}}),[M,x,O,k]);var B=null!==(n=null==x?void 0:x.startsWith("#"))&&void 0!==n&&n,U=!x||!k||B;return x&&k&&!B&&!b&&D.collectLink(x),U?o.createElement("a",Object.assign({href:x},A&&!k&&{target:"_blank",rel:"noopener noreferrer"},E)):o.createElement(V,Object.assign({},E,{onMouseEnter:function(){T.current||null==x||(window.docusaurus.preload(x),T.current=!0)},innerRef:function(e){var n,t;O&&e&&k&&(n=e,t=function(){null!=x&&window.docusaurus.prefetch(x)},M.current=new window.IntersectionObserver((function(e){e.forEach((function(e){n===e.target&&(e.isIntersecting||e.intersectionRatio>0)&&(M.current.unobserve(n),M.current.disconnect(),t())}))})),M.current.observe(n))},to:x||""},v&&{isActive:h,activeClassName:p}))}},95999:function(e,n,t){t.r(n),t.d(n,{default:function(){return s},translate:function(){return l}});var r=t(67294),o=/{\w+}/g,u="{}";function i(e,n){var t=[],i=e.replace(o,(function(e){var o=e.substr(1,e.length-2),i=null==n?void 0:n[o];if(void 0!==i){var a=r.isValidElement(i)?i:String(i);return t.push(a),u}return e}));return 0===t.length?e:t.every((function(e){return"string"==typeof e}))?i.split(u).reduce((function(e,n,r){var o;return e.concat(n).concat(null!==(o=t[r])&&void 0!==o?o:"")}),""):i.split(u).reduce((function(e,n,o){return[].concat(e,[r.createElement(r.Fragment,{key:o},n,t[o])])}),[])}var a=t(57529);function c(e){var n,t,r=e.id,o=e.message;if(void 0===r&&void 0===o)throw new Error("Docusaurus translation declarations must have at least a translation id or a default translation message");return null!==(t=null!==(n=a[null!=r?r:o])&&void 0!==n?n:o)&&void 0!==t?t:r}function l(e,n){return i(c({message:e.message,id:e.id}),n)}function s(e){var n=e.children,t=e.id,r=e.values;if(n&&"string"!=typeof n)throw console.warn("Illegal <Translate> children",n),new Error("The Docusaurus <Translate> component only accept simple string values");return i(c({message:n,id:t}),r)}},29935:function(e,n,t){t.d(n,{m:function(){return r}});var r="default"},13919:function(e,n,t){function r(e){return!0===/^(\w*:|\/\/)/.test(e)}function o(e){return void 0!==e&&!r(e)}t.d(n,{b:function(){return r},Z:function(){return o}})},28143:function(e,n,t){t.r(n),t.d(n,{BrowserRouter:function(){return r.VK},HashRouter:function(){return r.UT},Link:function(){return r.rU},MemoryRouter:function(){return r.VA},NavLink:function(){return r.OL},Prompt:function(){return r.NL},Redirect:function(){return r.l_},Route:function(){return r.AW},Router:function(){return r.F0},StaticRouter:function(){return r.gx},Switch:function(){return r.rs},generatePath:function(){return r.Gn},matchPath:function(){return r.LX},useHistory:function(){return r.k6},useLocation:function(){return r.TH},useParams:function(){return r.UO},useRouteMatch:function(){return r.$B},withRouter:function(){return r.EN}});var r=t(73727)},44996:function(e,n,t){t.r(n),t.d(n,{useBaseUrlUtils:function(){return u},default:function(){return i}});var r=t(52263),o=t(13919);function u(){var e=(0,r.default)().siteConfig,n=(e=void 0===e?{}:e).baseUrl,t=void 0===n?"/":n,u=e.url;return{withBaseUrl:function(e,n){return function(e,n,t,r){var u=void 0===r?{}:r,i=u.forcePrependBaseUrl,a=void 0!==i&&i,c=u.absolute,l=void 0!==c&&c;if(!t)return t;if(t.startsWith("#"))return t;if((0,o.b)(t))return t;if(a)return n+t;var s=t.startsWith(n)?t:n+t.replace(/^\//,"");return l?e+s:s}(u,t,e,n)}}}function i(e,n){return void 0===n&&(n={}),(0,u().withBaseUrl)(e,n)}},28084:function(e,n,t){t.r(n),t.d(n,{default:function(){return u},useAllPluginInstancesData:function(){return i},usePluginData:function(){return a}});var r=t(52263),o=t(29935);function u(){var e=(0,r.default)().globalData;if(!e)throw new Error("Docusaurus global data not found.");return e}function i(e){var n=u()[e];if(!n)throw new Error('Docusaurus plugin global data not found for "'+e+'" plugin.');return n}function a(e,n){void 0===n&&(n=o.m);var t=i(e)[n];if(!t)throw new Error('Docusaurus plugin global data not found for "'+e+'" plugin with id "'+n+'".');return t}},72389:function(e,n,t){t.r(n),t.d(n,{default:function(){return u}});var r=t(67294),o=t(9913);function u(){return(0,r.useContext)(o._)}},48408:function(e,n,t){Object.defineProperty(n,"__esModule",{value:!0}),n.getDocVersionSuggestions=n.getActiveDocContext=n.getActiveVersion=n.getLatestVersion=n.getActivePlugin=void 0;var r=t(28143);n.getActivePlugin=function(e,n,t){void 0===t&&(t={});var o=Object.entries(e).find((function(e){e[0];var t=e[1];return!!(0,r.matchPath)(n,{path:t.path,exact:!1,strict:!1})})),u=o?{pluginId:o[0],pluginData:o[1]}:void 0;if(!u&&t.failfast)throw new Error("Can't find active docs plugin for \""+n+'" pathname, while it was expected to be found. Maybe you tried to use a docs feature that can only be used on a docs-related page? Existing docs plugin paths are: '+Object.values(e).map((function(e){return e.path})).join(", "));return u};n.getLatestVersion=function(e){return e.versions.find((function(e){return e.isLast}))};n.getActiveVersion=function(e,t){var o=(0,n.getLatestVersion)(e);return[].concat(e.versions.filter((function(e){return e!==o})),[o]).find((function(e){return!!(0,r.matchPath)(t,{path:e.path,exact:!1,strict:!1})}))};n.getActiveDocContext=function(e,t){var o,u,i=(0,n.getActiveVersion)(e,t),a=null==i?void 0:i.docs.find((function(e){return!!(0,r.matchPath)(t,{path:e.path,exact:!0,strict:!1})}));return{activeVersion:i,activeDoc:a,alternateDocVersions:a?(o=a.id,u={},e.versions.forEach((function(e){e.docs.forEach((function(n){n.id===o&&(u[e.name]=n)}))})),u):{}}};n.getDocVersionSuggestions=function(e,t){var r=(0,n.getLatestVersion)(e),o=(0,n.getActiveDocContext)(e,t);return{latestDocSuggestion:null==o?void 0:o.alternateDocVersions[r.name],latestVersionSuggestion:r}}},96730:function(e,n,t){Object.defineProperty(n,"X$",{value:!0}),n.Jo=n.Iw=n.zu=n.yW=n.gB=n.WS=n.gA=n.zh=n._r=void 0;var r=t(70655),o=t(28143),u=(0,r.__importStar)(t(28084)),i=t(48408),a={};n._r=function(){var e;return null!==(e=(0,u.default)()["docusaurus-plugin-content-docs"])&&void 0!==e?e:a};n.zh=function(e){return(0,u.usePluginData)("docusaurus-plugin-content-docs",e)};n.gA=function(e){void 0===e&&(e={});var t=(0,n._r)(),r=(0,o.useLocation)().pathname;return(0,i.getActivePlugin)(t,r,e)};n.WS=function(e){void 0===e&&(e={});var t=(0,n.gA)(e),r=(0,o.useLocation)().pathname;if(t)return{activePlugin:t,activeVersion:(0,i.getActiveVersion)(t.pluginData,r)}};n.gB=function(e){return(0,n.zh)(e).versions};n.yW=function(e){var t=(0,n.zh)(e);return(0,i.getLatestVersion)(t)};n.zu=function(e){var t=(0,n.zh)(e),r=(0,o.useLocation)().pathname;return(0,i.getActiveVersion)(t,r)};n.Iw=function(e){var t=(0,n.zh)(e),r=(0,o.useLocation)().pathname;return(0,i.getActiveDocContext)(t,r)};n.Jo=function(e){var t=(0,n.zh)(e),r=(0,o.useLocation)().pathname;return(0,i.getDocVersionSuggestions)(t,r)}},41217:function(e,n,t){t.r(n),t.d(n,{default:function(){return a}});var r=t(67294),o=t(12859),u=t(89521),i=t(44996);function a(e){var n=e.title,t=e.description,a=e.keywords,c=e.image,l=e.children,s=(0,u.useTitleFormatter)(n),f=(0,i.useBaseUrlUtils)().withBaseUrl,d=c?f(c,{absolute:!0}):void 0;return r.createElement(o.Z,null,n&&r.createElement("title",null,s),n&&r.createElement("meta",{property:"og:title",content:s}),t&&r.createElement("meta",{name:"description",content:t}),t&&r.createElement("meta",{property:"og:description",content:t}),a&&r.createElement("meta",{name:"keywords",content:Array.isArray(a)?a.join(","):a}),d&&r.createElement("meta",{property:"og:image",content:d}),d&&r.createElement("meta",{name:"twitter:image",content:d}),l)}},80907:function(e,n,t){t.r(n),t.d(n,{__esModule:function(){return r.X$},useActiveDocContext:function(){return r.Iw},useActivePlugin:function(){return r.gA},useActivePluginAndVersion:function(){return r.WS},useActiveVersion:function(){return r.zu},useAllDocsData:function(){return r._r},useDocVersionSuggestions:function(){return r.Jo},useDocsData:function(){return r.zh},useLatestVersion:function(){return r.yW},useVersions:function(){return r.gB}});var r=t(96730)},89521:function(e,n,t){t.r(n),t.d(n,{AnnouncementBarProvider:function(){return Pe},Collapsible:function(){return z},DEFAULT_SEARCH_TAG:function(){return m},Details:function(){return G},DocsPreferredVersionContextProvider:function(){return le},MobileSecondaryMenuFiller:function(){return re},MobileSecondaryMenuProvider:function(){return ee},ScrollControllerProvider:function(){return Ue},ThemeClassNames:function(){return pe},createStorageSlot:function(){return l},docVersionSearchTag:function(){return p},duplicates:function(){return me},isDocsPluginEnabled:function(){return b},isRegexpStringMatch:function(){return He},isSamePath:function(){return w},listStorageKeys:function(){return s},listTagsByLetters:function(){return Ae},parseCodeBlockTitle:function(){return g},translateTagsPageTitle:function(){return De},useAlternatePageUtils:function(){return d},useAnnouncementBar:function(){return Ce},useCollapsible:function(){return B},useDocsPreferredVersion:function(){return ve},useDocsPreferredVersionByPluginId:function(){return ge},useDynamicCallback:function(){return k},useHistoryPopHandler:function(){return ke},useIsomorphicLayoutEffect:function(){return A},useLocalPathname:function(){return Le},useLocationChange:function(){return x},useMobileSecondaryMenuRenderer:function(){return te},usePluralForm:function(){return D},usePrevious:function(){return R},useScrollController:function(){return Ie},useScrollPosition:function(){return je},useScrollPositionBlocker:function(){return _e},useTOCFilter:function(){return Me},useTOCHighlight:function(){return Ve},useThemeConfig:function(){return o},useTitleFormatter:function(){return y}});var r=t(52263);function o(){return(0,r.default)().siteConfig.themeConfig}var u="localStorage";function i(e){if(void 0===e&&(e=u),"undefined"==typeof window)throw new Error("Browser storage is not available on Node.js/Docusaurus SSR process.");if("none"===e)return null;try{return window[e]}catch(t){return n=t,a||(console.warn("Docusaurus browser storage is not available.\nPossible reasons: running Docusaurus in an iframe, in an incognito browser session, or using too strict browser privacy settings.",n),a=!0),null}var n}var a=!1;var c={get:function(){return null},set:function(){},del:function(){}};var l=function(e,n){if("undefined"==typeof window)return function(e){function n(){throw new Error('Illegal storage API usage for storage key "'+e+'".\nDocusaurus storage APIs are not supposed to be called on the server-rendering process.\nPlease only call storage APIs in effects and event handlers.')}return{get:n,set:n,del:n}}(e);var t=i(null==n?void 0:n.persistence);return null===t?c:{get:function(){return t.getItem(e)},set:function(n){return t.setItem(e,n)},del:function(){return t.removeItem(e)}}};function s(e){void 0===e&&(e=u);var n=i(e);if(!n)return[];for(var t=[],r=0;r<n.length;r+=1){var o=n.key(r);null!==o&&t.push(o)}return t}var f=t(76775);function d(){var e=(0,r.default)(),n=e.siteConfig,t=n.baseUrl,o=n.url,u=e.i18n,i=u.defaultLocale,a=u.currentLocale,c=(0,f.TH)().pathname,l=a===i?t:t.replace("/"+a+"/","/"),s=c.replace(t,"");return{createUrl:function(e){var n=e.locale;return""+(e.fullyQualified?o:"")+function(e){return e===i?""+l:""+l+e+"/"}(n)+s}}}var v=/title=(["'])(.*?)\1/;function g(e){var n,t;return null!==(t=null===(n=null==e?void 0:e.match(v))||void 0===n?void 0:n[2])&&void 0!==t?t:""}var m="default";function p(e,n){return"docs-"+e+"-"+n}var h=t(80907),b=!!h.useAllDocsData,w=function(e,n){var t=function(e){return!e||(null==e?void 0:e.endsWith("/"))?e:e+"/"};return t(e)===t(n)},y=function(e){var n=(0,r.default)().siteConfig,t=n.title,o=n.titleDelimiter;return e&&e.trim().length?e.trim()+" "+o+" "+t:t},E=t(67294),P=["zero","one","two","few","many","other"];function C(e){return P.filter((function(n){return e.includes(n)}))}var L={locale:"en",pluralForms:C(["one","other"]),select:function(e){return 1===e?"one":"other"}};function S(){var e=(0,r.default)().i18n.currentLocale;return(0,E.useMemo)((function(){if(!Intl.PluralRules)return console.error("Intl.PluralRules not available!\nDocusaurus will fallback to a default/fallback (English) Intl.PluralRules implementation.\n        "),L;try{return n=e,t=new Intl.PluralRules(n),{locale:n,pluralForms:C(t.resolvedOptions().pluralCategories),select:function(e){return t.select(e)}}}catch(r){return console.error('Failed to use Intl.PluralRules for locale "'+e+'".\nDocusaurus will fallback to a default/fallback (English) Intl.PluralRules implementation.\n'),L}var n,t}),[e])}function D(){var e=S();return{selectMessage:function(n,t){return function(e,n,t){var r=e.split("|");if(1===r.length)return r[0];r.length>t.pluralForms.length&&console.error("For locale="+t.locale+", a maximum of "+t.pluralForms.length+" plural forms are expected ("+t.pluralForms+"), but the message contains "+r.length+" plural forms: "+e+" ");var o=t.select(n),u=t.pluralForms.indexOf(o);return r[Math.min(u,r.length-1)]}(t,n,e)}}}var A="undefined"!=typeof window?E.useLayoutEffect:E.useEffect;function k(e){var n=(0,E.useRef)(e);return A((function(){n.current=e}),[e]),(0,E.useCallback)((function(){return n.current.apply(n,arguments)}),[])}function R(e){var n=(0,E.useRef)();return A((function(){n.current=e})),n.current}function x(e){var n=(0,f.TH)(),t=R(n),r=k(e);(0,E.useEffect)((function(){r({location:n,previousLocation:t})}),[r,n,t])}var T=t(63366),V=t(10412),O=["collapsed"],M=["lazy"];function B(e){var n=e.initialState,t=(0,E.useState)(null!=n&&n),r=t[0],o=t[1],u=(0,E.useCallback)((function(){o((function(e){return!e}))}),[]);return{collapsed:r,setCollapsed:o,toggleCollapsed:u}}var U={display:"none",overflow:"hidden",height:"0px"},I={display:"block",overflow:"visible",height:"auto"};function N(e,n){var t=n?U:I;e.style.display=t.display,e.style.overflow=t.overflow,e.style.height=t.height}function j(e){var n=e.collapsibleRef,t=e.collapsed,r=e.animation,o=(0,E.useRef)(!1);(0,E.useEffect)((function(){var e,u=n.current;function i(){var e,n,t=u.scrollHeight,o=null!==(e=null==r?void 0:r.duration)&&void 0!==e?e:function(e){var n=e/36;return Math.round(10*(4+15*Math.pow(n,.25)+n/5))}(t);return{transition:"height "+o+"ms "+(null!==(n=null==r?void 0:r.easing)&&void 0!==n?n:"ease-in-out"),height:t+"px"}}function a(){var e=i();u.style.transition=e.transition,u.style.height=e.height}if(!o.current)return N(u,t),void(o.current=!0);return u.style.willChange="height",e=requestAnimationFrame((function(){t?(a(),requestAnimationFrame((function(){u.style.height=U.height,u.style.overflow=U.overflow}))):(u.style.display="block",requestAnimationFrame((function(){a()})))})),function(){return cancelAnimationFrame(e)}}),[n,t,r])}function _(e){if(!V.default.canUseDOM)return e?U:I}function H(e){var n=e.as,t=void 0===n?"div":n,r=e.collapsed,o=e.children,u=e.animation,i=e.onCollapseTransitionEnd,a=e.className,c=e.disableSSRStyle,l=(0,E.useRef)(null);return j({collapsibleRef:l,collapsed:r,animation:u}),E.createElement(t,{ref:l,style:c?void 0:_(r),onTransitionEnd:function(e){"height"===e.propertyName&&(N(l.current,r),null==i||i(r))},className:a},o)}function F(e){var n=e.collapsed,t=(0,T.Z)(e,O),r=(0,E.useState)(!n),o=r[0],u=r[1];(0,E.useLayoutEffect)((function(){n||u(!0)}),[n]);var i=(0,E.useState)(n),a=i[0],c=i[1];return(0,E.useLayoutEffect)((function(){o&&c(n)}),[o,n]),o?E.createElement(H,Object.assign({},t,{collapsed:a})):null}function z(e){var n=e.lazy,t=(0,T.Z)(e,M),r=n?F:H;return E.createElement(r,Object.assign({},t))}var W=t(72389),q=t(86010),Z="details_Q743",X="isBrowser_rWTL",J="collapsibleContent_K5uX",K=["summary","children"];function Y(e){return!!e&&("SUMMARY"===e.tagName||Y(e.parentElement))}function $(e,n){return!!e&&(e===n||$(e.parentElement,n))}var G=function(e){var n,t=e.summary,r=e.children,o=(0,T.Z)(e,K),u=(0,W.default)(),i=(0,E.useRef)(null),a=B({initialState:!o.open}),c=a.collapsed,l=a.setCollapsed,s=(0,E.useState)(o.open),f=s[0],d=s[1];return E.createElement("details",Object.assign({},o,{ref:i,open:f,"data-collapsed":c,className:(0,q.default)(Z,(n={},n[X]=u,n),o.className),onMouseDown:function(e){Y(e.target)&&e.detail>1&&e.preventDefault()},onClick:function(e){e.stopPropagation();var n=e.target;Y(n)&&$(n,i.current)&&(e.preventDefault(),c?(l(!1),d(!0)):l(!0))}}),t,E.createElement(z,{lazy:!1,collapsed:c,disableSSRStyle:!0,onCollapseTransitionEnd:function(e){l(e),d(!e)}},E.createElement("div",{className:J},r)))};var Q=(0,E.createContext)(null);function ee(e){var n=e.children;return E.createElement(Q.Provider,{value:(0,E.useState)(null)},n)}function ne(){var e=(0,E.useContext)(Q);if(null===e)throw new Error("MobileSecondaryMenuProvider was not used correctly, context value is null");return e}function te(){var e=ne()[0];if(e){var n=e.component;return function(t){return E.createElement(n,Object.assign({},e.props,t))}}return function(){}}function re(e){var n,t=e.component,r=e.props,o=ne()[1],u=(n=r,(0,E.useMemo)((function(){return n}),[].concat(Object.keys(n),Object.values(n))));return(0,E.useEffect)((function(){o({component:t,props:u})}),[o,t,u]),(0,E.useEffect)((function(){return function(){return o(null)}}),[o]),null}var oe=function(e){return"docs-preferred-version-"+e},ue={save:function(e,n,t){l(oe(e),{persistence:n}).set(t)},read:function(e,n){return l(oe(e),{persistence:n}).get()},clear:function(e,n){l(oe(e),{persistence:n}).del()}};function ie(e){var n=e.pluginIds,t=e.versionPersistence,r=e.allDocsData;var o={};return n.forEach((function(e){o[e]=function(e){var n=ue.read(e,t);return r[e].versions.some((function(e){return e.name===n}))?{preferredVersionName:n}:(ue.clear(e,t),{preferredVersionName:null})}(e)})),o}function ae(){var e=(0,h.useAllDocsData)(),n=o().docs.versionPersistence,t=(0,E.useMemo)((function(){return Object.keys(e)}),[e]),r=(0,E.useState)((function(){return function(e){var n={};return e.forEach((function(e){n[e]={preferredVersionName:null}})),n}(t)})),u=r[0],i=r[1];return(0,E.useEffect)((function(){i(ie({allDocsData:e,versionPersistence:n,pluginIds:t}))}),[e,n,t]),[u,(0,E.useMemo)((function(){return{savePreferredVersion:function(e,t){ue.save(e,n,t),i((function(n){var r;return Object.assign({},n,((r={})[e]={preferredVersionName:t},r))}))}}}),[n])]}var ce=(0,E.createContext)(null);function le(e){var n=e.children;return b?E.createElement(se,null,n):E.createElement(E.Fragment,null,n)}function se(e){var n=e.children,t=ae();return E.createElement(ce.Provider,{value:t},n)}function fe(){var e=(0,E.useContext)(ce);if(!e)throw new Error('Can\'t find docs preferred context, maybe you forgot to use the "DocsPreferredVersionContextProvider"?');return e}var de=t(29935);function ve(e){void 0===e&&(e=de.m);var n=(0,h.useDocsData)(e),t=fe(),r=t[0],o=t[1],u=r[e].preferredVersionName;return{preferredVersion:u?n.versions.find((function(e){return e.name===u})):null,savePreferredVersionName:(0,E.useCallback)((function(n){o.savePreferredVersion(e,n)}),[o,e])}}function ge(){var e=(0,h.useAllDocsData)(),n=fe()[0];var t=Object.keys(e),r={};return t.forEach((function(t){r[t]=function(t){var r=e[t],o=n[t].preferredVersionName;return o?r.versions.find((function(e){return e.name===o})):null}(t)})),r}function me(e,n){return void 0===n&&(n=function(e,n){return e===n}),e.filter((function(t,r){return e.findIndex((function(e){return n(e,t)}))!==r}))}var pe={page:{blogListPage:"blog-list-page",blogPostPage:"blog-post-page",blogTagsListPage:"blog-tags-list-page",blogTagPostListPage:"blog-tags-post-list-page",docsDocPage:"docs-doc-page",docsTagsListPage:"docs-tags-list-page",docsTagDocListPage:"docs-tags-doc-list-page",mdxPage:"mdx-page"},wrapper:{main:"main-wrapper",blogPages:"blog-wrapper",docsPages:"docs-wrapper",mdxPages:"mdx-wrapper"},common:{editThisPage:"theme-edit-this-page",lastUpdated:"theme-last-updated",backToTopButton:"theme-back-to-top-button"},layout:{},docs:{docVersionBanner:"theme-doc-version-banner",docVersionBadge:"theme-doc-version-badge",docMarkdown:"theme-doc-markdown",docTocMobile:"theme-doc-toc-mobile",docTocDesktop:"theme-doc-toc-desktop",docFooter:"theme-doc-footer",docFooterTagsRow:"theme-doc-footer-tags-row",docFooterEditMetaRow:"theme-doc-footer-edit-meta-row",docSidebarMenu:"theme-doc-sidebar-menu",docSidebarItemCategory:"theme-doc-sidebar-item-category",docSidebarItemLink:"theme-doc-sidebar-item-link",docSidebarItemCategoryLevel:function(e){return"theme-doc-sidebar-item-category-level-"+e},docSidebarItemLinkLevel:function(e){return"theme-doc-sidebar-item-link-level-"+e}},blog:{}},he=l("docusaurus.announcement.dismiss"),be=l("docusaurus.announcement.id"),we=function(){return"true"===he.get()},ye=function(e){return he.set(String(e))},Ee=(0,E.createContext)(null),Pe=function(e){var n=e.children,t=function(){var e=o().announcementBar,n=(0,W.default)(),t=(0,E.useState)((function(){return!!n&&we()})),r=t[0],u=t[1];(0,E.useEffect)((function(){u(we())}),[]);var i=(0,E.useCallback)((function(){ye(!0),u(!0)}),[]);return(0,E.useEffect)((function(){if(e){var n=e.id,t=be.get();"annoucement-bar"===t&&(t="announcement-bar");var r=n!==t;be.set(n),r&&ye(!1),!r&&we()||u(!1)}}),[e]),(0,E.useMemo)((function(){return{isActive:!!e&&!r,close:i}}),[e,r,i])}();return E.createElement(Ee.Provider,{value:t},n)},Ce=function(){var e=(0,E.useContext)(Ee);if(!e)throw new Error("useAnnouncementBar(): AnnouncementBar not found in React context: make sure to use the AnnouncementBarProvider on top of the tree");return e};function Le(){var e=(0,r.default)().siteConfig.baseUrl;return(0,f.TH)().pathname.replace(e,"/")}var Se=t(95999),De=function(){return(0,Se.translate)({id:"theme.tags.tagsPageTitle",message:"Tags",description:"The title of the tag list page"})};function Ae(e){var n={};return Object.values(e).forEach((function(e){var t,r=function(e){return e[0].toUpperCase()}(e.name);n[r]=null!==(t=n[r])&&void 0!==t?t:[],n[r].push(e)})),Object.entries(n).sort((function(e,n){var t=e[0],r=n[0];return t.localeCompare(r)})).map((function(e){return{letter:e[0],tags:e[1].sort((function(e,n){return e.name.localeCompare(n.name)}))}}))}function ke(e){!function(e){var n=(0,f.k6)().block,t=(0,E.useRef)(e);(0,E.useEffect)((function(){t.current=e}),[e]),(0,E.useEffect)((function(){return n((function(e,n){return t.current(e,n)}))}),[n,t])}((function(n,t){if("POP"===t)return e(n,t)}))}function Re(e){var n=e.getBoundingClientRect();return n.top===n.bottom?Re(e.parentNode):n}function xe(e,n){var t,r=n.anchorTopOffset,o=e.find((function(e){return Re(e).top>=r}));return o?function(e){return e.top>0&&e.bottom<window.innerHeight/2}(Re(o))?o:null!==(t=e[e.indexOf(o)-1])&&void 0!==t?t:null:e[e.length-1]}function Te(){var e=(0,E.useRef)(0),n=o().navbar.hideOnScroll;return(0,E.useEffect)((function(){e.current=n?0:document.querySelector(".navbar").clientHeight}),[n]),e}var Ve=function(e){var n=(0,E.useRef)(void 0),t=Te();(0,E.useEffect)((function(){if(!e)return function(){};var r=e.linkClassName,o=e.linkActiveClassName,u=e.minHeadingLevel,i=e.maxHeadingLevel;function a(){var e=function(e){return Array.from(document.getElementsByClassName(e))}(r),a=function(e){for(var n=e.minHeadingLevel,t=e.maxHeadingLevel,r=[],o=n;o<=t;o+=1)r.push("h"+o+".anchor");return Array.from(document.querySelectorAll(r.join()))}({minHeadingLevel:u,maxHeadingLevel:i}),c=xe(a,{anchorTopOffset:t.current}),l=e.find((function(e){return c&&c.id===function(e){return decodeURIComponent(e.href.substring(e.href.indexOf("#")+1))}(e)}));e.forEach((function(e){!function(e,t){var r;t?(n.current&&n.current!==e&&(null===(r=n.current)||void 0===r||r.classList.remove(o)),e.classList.add(o),n.current=e):e.classList.remove(o)}(e,e===l)}))}return document.addEventListener("scroll",a),document.addEventListener("resize",a),a(),function(){document.removeEventListener("scroll",a),document.removeEventListener("resize",a)}}),[e,t])};function Oe(e){var n=e.toc,t=e.minHeadingLevel,r=e.maxHeadingLevel;return n.flatMap((function(e){var n=Oe({toc:e.children,minHeadingLevel:t,maxHeadingLevel:r});return function(e){return e.level>=t&&e.level<=r}(e)?[Object.assign({},e,{children:n})]:n}))}function Me(e){var n=e.toc,t=e.minHeadingLevel,r=e.maxHeadingLevel;return(0,E.useMemo)((function(){return Oe({toc:n,minHeadingLevel:t,maxHeadingLevel:r})}),[n,t,r])}var Be=(0,E.createContext)(void 0);function Ue(e){var n,t=e.children;return E.createElement(Be.Provider,{value:(n=(0,E.useRef)(!0),(0,E.useMemo)((function(){return{scrollEventsEnabledRef:n,enableScrollEvents:function(){n.current=!0},disableScrollEvents:function(){n.current=!1}}}),[]))},t)}function Ie(){var e=(0,E.useContext)(Be);if(null==e)throw new Error('"useScrollController" is used but no context provider was found in the React tree.');return e}var Ne=function(){return V.default.canUseDOM?{scrollX:window.pageXOffset,scrollY:window.pageYOffset}:null};function je(e,n){void 0===n&&(n=[]);var t=Ie().scrollEventsEnabledRef,r=(0,E.useRef)(Ne()),o=k(e);(0,E.useEffect)((function(){var e=function(){if(t.current){var e=Ne();o&&o(e,r.current),r.current=e}},n={passive:!0};return e(),window.addEventListener("scroll",e,n),function(){return window.removeEventListener("scroll",e,n)}}),[o,t].concat(n))}function _e(){var e,n,t,r=Ie(),o=(e=(0,E.useRef)({elem:null,top:0}),n=(0,E.useCallback)((function(n){e.current={elem:n,top:n.getBoundingClientRect().top}}),[]),t=(0,E.useCallback)((function(){var n=e.current,t=n.elem,r=n.top;if(!t)return{restored:!1};var o=t.getBoundingClientRect().top-r;return o&&window.scrollBy({left:0,top:o}),e.current={elem:null,top:0},{restored:0!==o}}),[]),(0,E.useMemo)((function(){return{save:n,restore:t}}),[t,n])),u=(0,E.useRef)(void 0),i=(0,E.useCallback)((function(e){o.save(e),r.disableScrollEvents(),u.current=function(){var e=o.restore().restored;if(u.current=void 0,e){window.addEventListener("scroll",(function e(){r.enableScrollEvents(),window.removeEventListener("scroll",e)}))}else r.enableScrollEvents()}}),[r,o]);return(0,E.useLayoutEffect)((function(){var e;null===(e=u.current)||void 0===e||e.call(u)})),{blockElementScrollPositionUntilNextRender:i}}function He(e,n){return void 0!==e&&void 0!==n&&new RegExp(e,"gi").test(n)}},8802:function(e,n){Object.defineProperty(n,"__esModule",{value:!0}),n.default=function(e,n){var t=n.trailingSlash,r=n.baseUrl;if(e.startsWith("#"))return e;if(void 0===t)return e;var o,u=e.split(/[#?]/)[0],i="/"===u||u===r?u:(o=u,t?function(e){return e.endsWith("/")?e:e+"/"}(o):function(e){return e.endsWith("/")?e.slice(0,-1):e}(o));return e.replace(u,i)}},18780:function(e,n,t){var r=this&&this.__importDefault||function(e){return e&&e.__esModule?e:{default:e}};Object.defineProperty(n,"__esModule",{value:!0}),n.uniq=n.applyTrailingSlash=void 0;var o=t(8802);Object.defineProperty(n,"applyTrailingSlash",{enumerable:!0,get:function(){return r(o).default}});var u=t(29964);Object.defineProperty(n,"uniq",{enumerable:!0,get:function(){return r(u).default}})},29964:function(e,n){Object.defineProperty(n,"__esModule",{value:!0}),n.default=function(e){return Array.from(new Set(e))}},86010:function(e,n,t){function r(e){var n,t,o="";if("string"==typeof e||"number"==typeof e)o+=e;else if("object"==typeof e)if(Array.isArray(e))for(n=0;n<e.length;n++)e[n]&&(t=r(e[n]))&&(o&&(o+=" "),o+=t);else for(n in e)e[n]&&(o&&(o+=" "),o+=n);return o}function o(){for(var e,n,t=0,o="";t<arguments.length;)(e=arguments[t++])&&(n=r(e))&&(o&&(o+=" "),o+=n);return o}t.r(n),t.d(n,{default:function(){return o}})}}]);