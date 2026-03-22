/**
 * Adaline.ai 风格的页面转场动画
 * 为所有页面切换提供平滑的过渡效果
 */

(function() {
	'use strict';

	// 转场动画配置 - Adaline.ai 风格（带滑动效果）
	const TRANSITION_CONFIG = {
		duration: 10000,                  // 转场动画持续时间（毫秒）- 保留用于其他场景
		fadeInDuration: 50,              // 从下方飞入的持续时间（毫秒）
		fadeOutDuration: 300,            // 向上飞出的持续时间（毫秒）
		waitDuration: 550,               // 飞入后等待时间（毫秒）
		easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)', // 精致的缓动函数 - 类似 Adaline.ai
		fadeOutOpacity: 0,               // 淡出时的透明度
		fadeInOpacity: 1,                // 淡入时的透明度
		enableOnMobile: true,            // 是否在移动端启用
		excludePaths: ['#', 'javascript:', 'mailto:', 'tel:'], // 排除的链接类型
		skipTransition: false,           // 是否跳过转场（用于特殊场景）
		initialDelay: 200                // 初始加载延迟（毫秒）- 确保内容已渲染
	};

	// 创建转场覆盖层
	function createTransitionOverlay(initialVisible = false) {
		// 检查是否已经有内联创建的覆盖层
		let overlay = document.getElementById('page-transition-overlay-inline');
		
		if (overlay) {
			// 重命名 ID 并添加过渡效果
			overlay.id = 'page-transition-overlay';
			// 确保 transition 属性已设置（只动画 transform，不动画 opacity）
			overlay.style.transition = `transform ${TRANSITION_CONFIG.fadeInDuration}ms ${TRANSITION_CONFIG.easing}`;
			overlay.style.willChange = 'transform';
			overlay.style.backfaceVisibility = 'hidden';
			overlay.style.webkitBackfaceVisibility = 'hidden';
			overlay.style.transform = 'translateZ(0)'; // 硬件加速
			if (!initialVisible) {
				overlay.style.opacity = TRANSITION_CONFIG.fadeOutOpacity.toString();
				overlay.style.transform = 'translateY(-100%) translateZ(0)'; // 向上飞出
				overlay.style.pointerEvents = 'none';
			} else {
				overlay.style.opacity = TRANSITION_CONFIG.fadeInOpacity.toString();
				overlay.style.transform = 'translateY(0) translateZ(0)'; // 正常位置
				overlay.style.pointerEvents = 'auto';
			}
			return overlay;
		}
		
		// 创建新的覆盖层
		overlay = document.createElement('div');
		overlay.id = 'page-transition-overlay';
		// Adaline.ai 风格背景：简洁的白色到浅灰渐变
		const initialOpacity = initialVisible ? TRANSITION_CONFIG.fadeInOpacity : TRANSITION_CONFIG.fadeOutOpacity;
		const initialTransform = initialVisible ? 'translateY(0) translateZ(0)' : 'translateY(-100%) translateZ(0)';
		overlay.style.cssText = `
			position: fixed;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
			background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 50%, #f1f3f5 100%);
			z-index: 99999;
			opacity: ${initialOpacity};
			pointer-events: ${initialVisible ? 'auto' : 'none'};
			transition: transform ${TRANSITION_CONFIG.fadeInDuration}ms ${TRANSITION_CONFIG.easing};
			will-change: opacity, transform;
			backface-visibility: hidden;
			-webkit-backface-visibility: hidden;
			transform: ${initialTransform};
		`;
		// 确保 body 存在后再添加
		if (document.body) {
			document.body.appendChild(overlay);
		} else {
			document.documentElement.appendChild(overlay);
		}
		return overlay;
	}

	// 初始化转场覆盖层
	let transitionOverlay = null;
	
	// 立即查找内联创建的覆盖层
	function findOrCreateOverlay() {
		// 检查是否是首次页面加载（通过 sessionStorage 标记）
		const isFirstLoad = !sessionStorage.getItem('page-transition-initialized');
		const isFromTransition = sessionStorage.getItem('page-transition-pending') === 'true';
		
		// 首次加载或从其他页面跳转过来时，覆盖层应该可见
		const shouldShowOverlay = isFirstLoad || isFromTransition;
		
		// 尝试查找内联创建的覆盖层
		let overlay = document.getElementById('page-transition-overlay-inline');
		if (!overlay) {
			// 如果没找到，尝试查找已重命名的覆盖层
			overlay = document.getElementById('page-transition-overlay');
		}
		
		if (overlay) {
			transitionOverlay = overlay;
			// 确保 ID 正确
			if (overlay.id === 'page-transition-overlay-inline') {
				overlay.id = 'page-transition-overlay';
			}
			// 确保样式正确（只动画 transform，不动画 opacity）
			const transitionValue = `transform ${TRANSITION_CONFIG.fadeInDuration}ms ${TRANSITION_CONFIG.easing}`;
			overlay.style.transition = transitionValue;
			overlay.style.willChange = 'transform';
			overlay.style.backfaceVisibility = 'hidden';
			overlay.style.webkitBackfaceVisibility = 'hidden';
			
			// 确保初始状态正确
			if (shouldShowOverlay) {
				overlay.style.opacity = TRANSITION_CONFIG.fadeInOpacity.toString();
				overlay.style.transform = 'translateY(0) translateZ(0)';
				overlay.style.pointerEvents = 'auto';
			} else {
				overlay.style.opacity = TRANSITION_CONFIG.fadeOutOpacity.toString();
				overlay.style.transform = 'translateY(-100%) translateZ(0)';
				overlay.style.pointerEvents = 'none';
			}
		} else {
			// 如果都没找到，创建新的
			transitionOverlay = createTransitionOverlay(shouldShowOverlay);
		}
		
		if (isFirstLoad) {
			sessionStorage.setItem('page-transition-initialized', 'true');
		}
	}
	
	// 立即尝试查找或创建覆盖层
	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', findOrCreateOverlay);
	} else {
		findOrCreateOverlay();
	}

	// 检查是否应该跳过转场
	function shouldSkipTransition(url) {
		if (TRANSITION_CONFIG.skipTransition) return true;
		
		// 检查是否是 account 路由（禁用转场动画）
		if (url.includes('/account') || window.location.pathname.startsWith('/account')) {
			return true;
		}
		
		// 检查是否是外部链接
		if (url.startsWith('http://') || url.startsWith('https://')) {
			try {
				const linkUrl = new URL(url);
				const currentUrl = new URL(window.location.href);
				if (linkUrl.origin !== currentUrl.origin) {
					return true; // 外部链接，跳过转场
				}
			} catch (e) {
				return true;
			}
		}

		// 检查是否是排除的路径
		for (const excludePath of TRANSITION_CONFIG.excludePaths) {
			if (url.startsWith(excludePath)) {
				return true;
			}
		}

		// 检查是否是锚点链接（同一页面内跳转）
		if (url.startsWith('#')) {
			return true;
		}

		return false;
	}

	// 淡出动画（页面切换时，显示覆盖层 - 从下方飞入）
	function fadeOut(callback) {
		if (!transitionOverlay) {
			transitionOverlay = createTransitionOverlay(true);
		}
		
		// 确保 transition 属性已设置（只动画 transform，不动画 opacity）
		const transitionValue = `transform ${TRANSITION_CONFIG.fadeInDuration}ms ${TRANSITION_CONFIG.easing}`;
		transitionOverlay.style.transition = transitionValue;
		transitionOverlay.style.willChange = 'transform';
		
		// 先设置初始位置（在屏幕下方），保持完全不透明
		transitionOverlay.style.transform = 'translateY(100%) translateZ(0)';
		transitionOverlay.style.opacity = TRANSITION_CONFIG.fadeInOpacity.toString(); // 保持完全不透明
		transitionOverlay.style.pointerEvents = 'auto';
		
		// 确保覆盖层在最上层
		transitionOverlay.style.zIndex = '99999';
		
		// 强制重排，然后触发动画
		transitionOverlay.offsetHeight;
		requestAnimationFrame(() => {
			requestAnimationFrame(() => {
				// 从下方飞入到正常位置，保持完全不透明
				transitionOverlay.style.transform = 'translateY(0) translateZ(0)';
				transitionOverlay.style.opacity = TRANSITION_CONFIG.fadeInOpacity.toString();
			});
		});
		
		if (callback) {
			setTimeout(callback, TRANSITION_CONFIG.fadeInDuration);
		}
	}

	// 淡入动画（覆盖层向上飞出）
	function fadeIn() {
		if (!transitionOverlay) {
			console.warn('Transition overlay not found in fadeIn');
			return;
		}
		
		// 确保 transition 属性已设置（只动画 transform，不动画 opacity）
		const transitionValue = `transform ${TRANSITION_CONFIG.fadeOutDuration}ms ${TRANSITION_CONFIG.easing}`;
		transitionOverlay.style.transition = transitionValue;
		transitionOverlay.style.willChange = 'transform';
		
		// 确保当前状态是可见的（正常位置），保持完全不透明
		transitionOverlay.style.opacity = TRANSITION_CONFIG.fadeInOpacity.toString();
		transitionOverlay.style.transform = 'translateY(0) translateZ(0)';
		
		// 强制重排，确保 transition 生效
		transitionOverlay.offsetHeight;
		
		// 触发向上飞出动画
		requestAnimationFrame(() => {
			if (!transitionOverlay) return;
			
			// 再次强制重排
			transitionOverlay.offsetHeight;
			
			requestAnimationFrame(() => {
				if (!transitionOverlay) return;
				
				// 向上飞出，保持完全不透明
				transitionOverlay.style.transform = 'translateY(-100%) translateZ(0)';
				transitionOverlay.style.opacity = TRANSITION_CONFIG.fadeInOpacity.toString();
			});
		});
		
		setTimeout(() => {
			if (transitionOverlay) {
				transitionOverlay.style.pointerEvents = 'none';
			}
		}, TRANSITION_CONFIG.fadeOutDuration);
	}

	// 处理链接点击
	function handleLinkClick(e) {
		const link = e.currentTarget;
		const href = link.getAttribute('href');
		
		if (!href || shouldSkipTransition(href)) {
			return; // 跳过转场
		}

		// 检查是否是表单提交或其他特殊操作
		if (link.hasAttribute('download') || 
			link.hasAttribute('target') && link.getAttribute('target') === '_blank') {
			return; // 下载链接或新窗口链接，跳过转场
		}

		// 阻止默认行为
		e.preventDefault();
		
		// 标记即将进行页面转场
		sessionStorage.setItem('page-transition-pending', 'true');
		
		// 执行转场动画
		fadeOut(() => {
			// 转场完成后跳转
			window.location.href = href;
		});
	}

	// 页面加载时的淡入动画（覆盖层从下方飞入，然后向上飞出）
	function initPageLoadAnimation() {
		// 检查是否是 account 路由（禁用转场动画）
		if (window.location.pathname.startsWith('/account')) {
			if (transitionOverlay) {
				transitionOverlay.style.opacity = TRANSITION_CONFIG.fadeOutOpacity.toString();
				transitionOverlay.style.transform = 'translateY(-100%) translateZ(0)';
				transitionOverlay.style.pointerEvents = 'none';
			}
			return;
		}
		
		// 检查是否是浏览器前进/后退导航
		const isBackForward = window.performance && 
			window.performance.navigation && 
			window.performance.navigation.type === 2;
		
		// 如果是前进/后退，跳过初始动画
		if (isBackForward) {
			if (transitionOverlay) {
				transitionOverlay.style.opacity = TRANSITION_CONFIG.fadeOutOpacity.toString();
				transitionOverlay.style.transform = 'translateY(-100%) translateZ(0)';
				transitionOverlay.style.pointerEvents = 'none';
			}
			return;
		}

		// 检查是否是从其他页面跳转过来
		const isFromTransition = sessionStorage.getItem('page-transition-pending') === 'true';
		
		// 如果覆盖层不存在，创建它（应该已经创建了，但以防万一）
		if (!transitionOverlay) {
			transitionOverlay = createTransitionOverlay(true);
		}
		
		// 确保覆盖层存在
		if (!transitionOverlay) {
			console.warn('Page transition overlay not found');
			return;
		}
		
		// 确保覆盖层有 transition 属性（只动画 transform，不动画 opacity）
		// 设置为飞出动画的 transition
		const fadeOutTransition = `transform ${TRANSITION_CONFIG.fadeOutDuration}ms ${TRANSITION_CONFIG.easing}`;
		transitionOverlay.style.transition = fadeOutTransition;
		transitionOverlay.style.willChange = 'transform';
		transitionOverlay.style.backfaceVisibility = 'hidden';
		transitionOverlay.style.webkitBackfaceVisibility = 'hidden';
		transitionOverlay.style.zIndex = '99999';
		
		// 清除转场标记
		if (isFromTransition) {
			sessionStorage.removeItem('page-transition-pending');
		}
		
		// 初始状态：遮罩直接遮住整个页面（正常位置，保持完全不透明）
		transitionOverlay.style.opacity = TRANSITION_CONFIG.fadeInOpacity.toString();
		transitionOverlay.style.transform = 'translateY(0) translateZ(0)';
		transitionOverlay.style.pointerEvents = 'auto';
		
		// 延迟确保页面内容已加载
		setTimeout(() => {
			// 确保覆盖层仍然存在
			if (!transitionOverlay) {
				console.warn('Transition overlay disappeared before animation');
				return;
			}
			
			// 等待指定时间后向上飞出
			setTimeout(() => {
				if (!transitionOverlay) return;
				
				// 强制重排
				transitionOverlay.offsetHeight;
				
				requestAnimationFrame(() => {
					if (!transitionOverlay) return;
					
					transitionOverlay.offsetHeight;
					
					requestAnimationFrame(() => {
						if (!transitionOverlay) return;
						
						// 向上飞出（200ms），保持完全不透明
						transitionOverlay.style.transform = 'translateY(-100%) translateZ(0)';
						transitionOverlay.style.opacity = TRANSITION_CONFIG.fadeInOpacity.toString();
						
						// 动画完成后隐藏
						setTimeout(() => {
							if (transitionOverlay) {
								transitionOverlay.style.pointerEvents = 'none';
							}
						}, TRANSITION_CONFIG.fadeOutDuration);
					});
				});
			}, TRANSITION_CONFIG.waitDuration); // 等待550ms
		}, TRANSITION_CONFIG.initialDelay); // 使用配置的延迟时间
	}

	// 绑定所有内部链接
	function bindLinks() {
		// 检查是否在移动端且禁用
		const isMobile = window.innerWidth <= 768;
		if (!TRANSITION_CONFIG.enableOnMobile && isMobile) {
			return;
		}

		// 选择所有内部链接
		const links = document.querySelectorAll('a[href]');
		
		links.forEach(link => {
			// 移除旧的事件监听器（如果存在）
			link.removeEventListener('click', handleLinkClick);
			// 添加新的事件监听器
			link.addEventListener('click', handleLinkClick);
		});
	}

	// 监听 DOM 变化，动态绑定新添加的链接
	function observeDOM() {
		const observer = new MutationObserver(() => {
			bindLinks();
		});

		observer.observe(document.body, {
			childList: true,
			subtree: true
		});
	}

	// 初始化
	function init() {
		// 页面加载动画
		if (document.readyState === 'loading') {
			document.addEventListener('DOMContentLoaded', () => {
				initPageLoadAnimation();
				bindLinks();
				observeDOM();
			});
		} else {
			initPageLoadAnimation();
			bindLinks();
			observeDOM();
		}

		// 监听浏览器前进/后退按钮
		window.addEventListener('pageshow', (e) => {
			if (e.persisted) {
				// 从缓存恢复的页面，跳过动画
				if (transitionOverlay) {
					transitionOverlay.style.opacity = TRANSITION_CONFIG.fadeOutOpacity.toString();
					transitionOverlay.style.transform = 'translateY(-100%) translateZ(0)';
					transitionOverlay.style.pointerEvents = 'none';
				}
			}
		});

		// 监听页面隐藏（用于优化转场）
		window.addEventListener('pagehide', () => {
			// 页面隐藏时保持覆盖层可见
			if (transitionOverlay) {
				transitionOverlay.style.opacity = TRANSITION_CONFIG.fadeInOpacity.toString();
				transitionOverlay.style.transform = 'translateY(0) translateZ(0)';
				transitionOverlay.style.pointerEvents = 'auto';
			}
		});
	}

	// 启动
	init();

	// 导出配置函数（用于外部调整）
	window.setPageTransitionConfig = function(config) {
		Object.assign(TRANSITION_CONFIG, config);
	};

	// 手动触发转场（用于特殊场景）
	window.triggerPageTransition = function(url) {
		if (shouldSkipTransition(url)) {
			window.location.href = url;
			return;
		}
		
		fadeOut(() => {
			window.location.href = url;
		});
	};

})();

