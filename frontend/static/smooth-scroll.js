/**
 * 全局滑动阻尼效果 - 增强版
 * 为所有页面提供明显的平滑滚动和阻尼效果
 */

(function() {
	'use strict';

	// 平滑滚动配置 - 适中的阻尼效果
	const SCROLL_CONFIG = {
		damping: 0.08,        // 阻尼系数 (降低以减弱阻尼感)
		wheelDamping: 0.6,    // 滚轮阻尼系数 (降低，让滚动更流畅)
		momentumDamping: 0.95, // 惯性滚动阻尼 (0.95 = 每帧减少5%速度，惯性更强)
		duration: 600,        // 动画持续时间(ms)
		easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)' // 缓动函数
	};

	// 检查是否支持平滑滚动
	const supportsSmoothScroll = 'scrollBehavior' in document.documentElement.style;

	// 如果浏览器不支持平滑滚动，使用 polyfill
	if (!supportsSmoothScroll) {
		const smoothScrollTo = function(element, target, duration) {
			const start = element.scrollTop;
			const distance = target - start;
			let startTime = null;

			function easeInOutCubic(t) {
				return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
			}

			function animation(currentTime) {
				if (startTime === null) startTime = currentTime;
				const timeElapsed = currentTime - startTime;
				const progress = Math.min(timeElapsed / duration, 1);
				const ease = easeInOutCubic(progress);
				element.scrollTop = start + distance * ease;
				if (timeElapsed < duration) {
					requestAnimationFrame(animation);
				}
			}

			requestAnimationFrame(animation);
		};

		document.addEventListener('click', function(e) {
			const target = e.target.closest('a[href^="#"]');
			if (target && target.getAttribute('href') !== '#') {
				const id = target.getAttribute('href').substring(1);
				const element = document.getElementById(id);
				if (element) {
					e.preventDefault();
					smoothScrollTo(document.documentElement, element.offsetTop, SCROLL_CONFIG.duration);
				}
			}
		});
	}

	// ========== 鼠标滚轮阻尼效果 - 增强版 ==========
	let isWheeling = false;
	let wheelAccumulator = 0;
	let wheelAnimationFrame = null;
	let currentScrollPosition = 0;
	let targetScrollPosition = 0;
	let scrollVelocity = 0;

	function smoothWheelScroll() {
		const diff = targetScrollPosition - currentScrollPosition;
		
		// 如果距离很小，直接跳转
		if (Math.abs(diff) < 0.5) {
			currentScrollPosition = targetScrollPosition;
			window.scrollTo(0, currentScrollPosition);
			isWheeling = false;
			return;
		}
		
		// 使用缓动函数进行平滑滚动
		const ease = 0.25; // 缓动系数，增大以降低阻尼感，让滚动更直接
		currentScrollPosition += diff * ease;
		
		// 应用阻尼
		scrollVelocity = diff * ease;
		scrollVelocity *= SCROLL_CONFIG.momentumDamping;
		
		window.scrollTo(0, currentScrollPosition);
		
		wheelAnimationFrame = requestAnimationFrame(smoothWheelScroll);
	}

	document.addEventListener('wheel', function(e) {
		// 阻止默认滚动行为
		e.preventDefault();
		
		// 更新当前和目标滚动位置
		currentScrollPosition = window.pageYOffset || document.documentElement.scrollTop;
		
		// 计算滚动增量，应用阻尼
		const delta = e.deltaY * SCROLL_CONFIG.wheelDamping;
		targetScrollPosition = currentScrollPosition + delta;
		
		// 限制滚动范围
		const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
		targetScrollPosition = Math.max(0, Math.min(maxScroll, targetScrollPosition));
		
		// 如果还没有开始滚动动画，启动它
		if (!isWheeling) {
			isWheeling = true;
			smoothWheelScroll();
		}
	}, { passive: false });

	// ========== 触摸滚动阻尼效果 - 增强版 ==========
	let touchStartY = 0;
	let touchStartX = 0;
	let isScrolling = false;
	let touchScrollVelocity = 0;
	let lastTouchTime = 0;
	let lastTouchY = 0;
	let touchMomentumAnimation = null;

	function calculateTouchVelocity(currentY) {
		const now = Date.now();
		if (lastTouchTime > 0) {
			const timeDelta = now - lastTouchTime;
			const yDelta = currentY - lastTouchY;
			if (timeDelta > 0) {
				touchScrollVelocity = -yDelta / timeDelta * 16; // 转换为像素/帧
			}
		}
		lastTouchTime = now;
		lastTouchY = currentY;
	}

	function applyTouchMomentum() {
		if (Math.abs(touchScrollVelocity) > 0.1) {
			const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
			const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
			
			// 应用阻尼
			touchScrollVelocity *= SCROLL_CONFIG.momentumDamping;
			
			// 计算新位置
			let newScroll = currentScroll + touchScrollVelocity;
			newScroll = Math.max(0, Math.min(maxScroll, newScroll));
			
			window.scrollTo(0, newScroll);
			
			// 如果到达边界，停止
			if (newScroll <= 0 || newScroll >= maxScroll) {
				touchScrollVelocity = 0;
			}
			
			if (Math.abs(touchScrollVelocity) > 0.1) {
				touchMomentumAnimation = requestAnimationFrame(applyTouchMomentum);
			} else {
				touchMomentumAnimation = null;
			}
		}
	}

	document.addEventListener('touchstart', function(e) {
		touchStartY = e.touches[0].clientY;
		touchStartX = e.touches[0].clientX;
		isScrolling = false;
		touchScrollVelocity = 0;
		lastTouchTime = Date.now();
		lastTouchY = touchStartY;
		
		// 停止之前的惯性滚动
		if (touchMomentumAnimation) {
			cancelAnimationFrame(touchMomentumAnimation);
			touchMomentumAnimation = null;
		}
	}, { passive: true });

	document.addEventListener('touchmove', function(e) {
		if (!isScrolling) {
			const deltaY = Math.abs(e.touches[0].clientY - touchStartY);
			const deltaX = Math.abs(e.touches[0].clientX - touchStartX);
			isScrolling = deltaY > deltaX && deltaY > 10;
		}
		
		if (isScrolling) {
			calculateTouchVelocity(e.touches[0].clientY);
		}
	}, { passive: true });

	document.addEventListener('touchend', function(e) {
		if (isScrolling && Math.abs(touchScrollVelocity) > 2) {
			applyTouchMomentum();
		}
		isScrolling = false;
	}, { passive: true });

	// ========== 键盘滚动阻尼效果 ==========
	let keyScrollVelocity = 0;
	const KEY_SCROLL_SPEED = 80; // 增加键盘滚动速度
	let keyAnimationFrame = null;

	function applyKeyScroll() {
		if (Math.abs(keyScrollVelocity) > 0.1) {
			const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
			const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
			
			// 应用阻尼
			keyScrollVelocity *= SCROLL_CONFIG.momentumDamping;
			
			let newScroll = currentScroll + keyScrollVelocity;
			newScroll = Math.max(0, Math.min(maxScroll, newScroll));
			
			window.scrollTo({
				top: newScroll,
				behavior: 'smooth'
			});
			
			if (Math.abs(keyScrollVelocity) > 0.1) {
				keyAnimationFrame = requestAnimationFrame(applyKeyScroll);
			} else {
				keyAnimationFrame = null;
			}
		}
	}

	document.addEventListener('keydown', function(e) {
		if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
			return;
		}

		let scrollDirection = 0;
		if (e.key === 'ArrowDown' || e.key === 'PageDown') {
			scrollDirection = 1;
			e.preventDefault();
		} else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
			scrollDirection = -1;
			e.preventDefault();
		} else if (e.key === 'Home') {
			window.scrollTo({ top: 0, behavior: 'smooth' });
			return;
		} else if (e.key === 'End') {
			window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'smooth' });
			return;
		}

		if (scrollDirection !== 0) {
			// 停止之前的滚动
			if (keyAnimationFrame) {
				cancelAnimationFrame(keyAnimationFrame);
			}
			
			keyScrollVelocity = scrollDirection * KEY_SCROLL_SPEED;
			applyKeyScroll();
		}
	}, { passive: false });

	// ========== 为所有可滚动容器添加阻尼效果 ==========
	function addDampingToScrollableElements() {
		const scrollableElements = document.querySelectorAll('*');
		scrollableElements.forEach(function(element) {
			const style = window.getComputedStyle(element);
			if (style.overflowY === 'scroll' || style.overflowY === 'auto' || 
			    style.overflow === 'scroll' || style.overflow === 'auto') {
				element.style.scrollBehavior = 'smooth';
				element.style.webkitOverflowScrolling = 'touch';
				element.style.overscrollBehavior = 'contain';
			}
		});
	}

	// 页面加载完成后应用效果
	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', function() {
			addDampingToScrollableElements();
			// 初始化滚动位置
			currentScrollPosition = window.pageYOffset || document.documentElement.scrollTop;
			targetScrollPosition = currentScrollPosition;
		});
	} else {
		addDampingToScrollableElements();
		currentScrollPosition = window.pageYOffset || document.documentElement.scrollTop;
		targetScrollPosition = currentScrollPosition;
	}

	// 监听动态添加的元素
	const observer = new MutationObserver(function(mutations) {
		mutations.forEach(function(mutation) {
			if (mutation.addedNodes.length > 0) {
				addDampingToScrollableElements();
			}
		});
	});

	observer.observe(document.body, {
		childList: true,
		subtree: true
	});

	// 导出配置（可选，用于外部调整）
	window.SmoothScrollConfig = SCROLL_CONFIG;
	
	// 提供手动调整阻尼的方法
	window.setScrollDamping = function(damping) {
		if (damping >= 0 && damping <= 1) {
			SCROLL_CONFIG.damping = damping;
			SCROLL_CONFIG.wheelDamping = damping * 2;
			console.log('滚动阻尼已更新:', damping);
		}
	};
})();
